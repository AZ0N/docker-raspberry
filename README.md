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
Refer to the section of each service installation:
- [OpenVPN](##openvpn)
- [Pihole](##pihole)
- [Jellyfin](##jellyfin)
- [Samba](##samba)
- [wakeonlan](##wakeonlan)
- [Docker setup](##docker-setup)
## Openvpn
## Pihole
## Jellyfin
## SAMBA
## wakeonlan
## Docker setup