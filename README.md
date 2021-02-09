# Raspberry Pi Home Server Setup

My setup includes the following services running on the Raspberry Pi 4B:
- **OpenVPN** through PiVPN
- **Pihole** for DNS-level ad-blocking
- **Samba** file server
- **wakeonlan** for waking local devices
- **Jellyfin** for media-streaming

The following services runs inside docker containers:
- **Grafana** for graphing system and network stats
- **InfluxDB** saving stats
- **Portainer** for managing Docker-containers
- **NGINX** as reverse proxy and static website
- **Python3** for datacollection *(not in container, but sends data to InfluxDB)*

## Web interface - Static website
![Web interface](https://i.imgur.com/R73QMmw.png)
## Grafana Interface - System and network stats
![Grafana Interface](https://i.imgur.com/PIl3FM9.png)

# Installation
I have used Raspberry Pi OS Lite, but the project can be applied to other distributions.

Refer to the section of each service installation:
- [OpenVPN](#openvpn)
- [Pihole](#pihole)
- [Jellyfin](#jellyfin)
- [Samba](#samba)
- [wakeonlan](#wakeonlan)
- [Docker setup](#docker-setup)
## OpenVPN
We will use PiVPN to install a OpenVPN server on the Pi. As decribed on the [PiVVPN Website](https://www.pivpn.io/):
```bash
curl -L https://install.pivpn.io | bash
```
This starts the installation. Here a dynamic DNS entry can be configured for accessing the VPN server. For more information about PiVPN, [see their documentation](https://docs.pivpn.io/). For accessing outside the local network, the chosen port needs to be forwared to the Raspberry Pi in the local routers configuration.
## Pihole
Pihole can be installed with the command:
```bash
curl -sSL https://install.pi-hole.net | bash
```
as described om the [Pihole Github Page](https://github.com/pi-hole/pi-hole). The interface can be accessed on ``http://raspberrypi/admin`` with the passsword showed in the terminal.

The password can be changed with the command:
```bash
sudo pihole -a -p
```
For setup with NGINX reverse-proxy, the port of the admin interface needs to be changed to 8080:
```bash
sudo nano /etc/lighttpd/lighttpd.conf
```
Where ``server.port`` has to be changed to 8080.

For compatibility with the NGINX reverse proxy, a virtual host need to be configured. The interface can be accessed without, but trying to change settings will throw an error, if not configured. Add the following line:
```
setenv.add-environment = ( "VIRTUAL_HOST" => "raspberrypi" )
```
to ``/etc/lighttpd/external.conf``

Substitute *raspberrypi* for the desired hostname.

Restart the lighttpd service:
```bash
sudo service lighttpd restart
```
## Jellyfin
Jellyfin is an open-source mediastreaming server. To isntall Jellyfin, use the following command:
```
sudo apt install apt-transport-https
wget -O - https://repo.jellyfin.org/jellyfin_team.gpg.key | sudo apt-key add -
echo "deb [arch=$( dpkg --print-architecture )] https://repo.jellyfin.org/$( awk -F'=' '/^ID=/{ print $NF }' /etc/os-release ) $( awk -F'=' '/^VERSION_CODENAME=/{ print $NF }' /etc/os-release ) main" | sudo tee /etc/apt/sources.list.d/jellyfin.list
sudo apt update
sudo apt install jellyfin
```
also shown on the [Jellyfin webiste](https://jellyfin.org/downloads/).

After installation, the Jellyfin user needs to be added to the video group:
```bash
sudo usermod +aG video jellyfin
```
The Jellyfin service need to restart:
```bash
sudo systemctl restart jellyfin
```
If 4K video-playback is needed, the GPU-memory needs to be atleast 320mb. This can be changed in ``/boot/config.txt``.

Add ``gpu_mem=amount`` to the bottom of the file. The system needs to be rebooted for the changes to take effect.

The Jellyfin web-interface can be located at ``http://raspberrypi:8096``. When accessing the interface for the first time, the interface will take you through some simple configuration. Her the credentialts for loggin into the webinterface is set.

For compability with the NGINX reverse-proxy subdirectory the ``base-url`` of the Jellyfin configuration need to be changed. The setting can be located in the web-interface by navigating to *Dashboard → Networking → Server Adress Settings* and setting the *Base URL* field to *jellyfin* to enable accessing the interface from the ``/jellyfin`` subdirectory.

If you are using a Raspberry Pi 4B, hardware acceleration can be enabled *Dashboard → Playback* and choosing *OpenMAX OMX* under hardware acceleration.
## Samba
Samba can be installed using apt:
```bash
sudo apt-get install samba samba-common-bin
```
Thereafter the configuration file can be edited using nano:
```bash
sudo nano /etc/samba/smb.conf
```
At the bottom the configuration file add the following:
```
[nameofshare]
path = /path/to/shared/directory
writeable=Yes
create mask=0777
directory mask=0777
public=no
```
Substitute the name of path to the desired shared folder.
The share can be accessed at ``//raspberrypi/nameofshare`` or at the ip-adress of the Pi.

Before accessing the share, a Samba user needs to be created. Choose a password for the user:
```bash
sudo smbpasswd -a pi
```
Finally restart the Samba service:
```bash
sudo systemctl restart smbd
```
## wakeonlan
The ``wakeonlan`` package can be installed using apt:
```bash
sudo apt install wakeonlan
```
Usage:
```bash
wakeonlan 00:11:22:33:44:55:66
```
where 00:11:22:33:44:55:66 is the MAC-adress of the device to wake.

Alternatively a bash script can be used instead of manually remembering the MAC-adress:
```sh
#!\bin\bash
wakeonlan 00:11:22:33:44:55:66
```
## Docker setup