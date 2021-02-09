# Raspberry Pi Home Server Setup

My setup includes the following services running on the Raspberry Pi 4B:
- **OpenVPN** through PiVPN
- **Pihole** for DNS-level ad-blocking
- **SAMBA** file server
- **wakeonlan**
- **Jellyfin** for media-streaming

The following services runs inside docker containers:
- **Grafana** for graphing system and network stats
- **InfluxDB** saving stats
- **Portainer** for managing Docker-containers
- **NGINX** as reverse proxy to access
- **Python3** for datacollection *(not in container, but sends data to InfluxDB)*

## Web interface
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
## Pihole
## Jellyfin
## SAMBA
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