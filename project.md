# Raspberry Pi 

## Local installation:
- OpenVPN med PIVPN
- Fail2Ban
- UFW
- wakeonlan
- Pihole + Unbound
- Jellyfin
- SAMBA

## Docker-containers

### Compose:
- NGINX - Reverse-proxy
- Grafana
- InfluxDB
- Portainer

### Other containers:
- Python data collection

# Oder of Operations
!## Raspiberry Pi Configuration
- Install newest Raspberry Pi OS (preferably 64-bit)
- Change password and sudo raspi-config for locale
- Mount external harddrive at /mnt/media

## Docker and docker compose
- Install docker: https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl
- Install compose: 
    sudo pip3 -v install docker-compose
- Clone repository:
    git clone https://github.com/AZ0N/docker-raspberry

- Change influx user password (and admin) and update in datacollection scripts
- Start the compose:
    docker-compose up -d
- Check web-interfaces
- Create Grafana password
- Connect InfluxDB database
- Create python datacollection container and test it connects to InfluxDB:
    
    SYSTEM INFO
    docker run --network main-network \
    -v $PWD/datacollection-python:/src \
    -v /proc:/host/proc:ro \
    --name systemdata \
    python_data_tag \
    python3 /src/data-system.py

    NETWORK INFO
    docker run --network main-network \
    -v $PWD/datacollection-python:/src\
    --name networkdata python_data_tag\
    python3 /src/data-speedtest.py

- Setup cronjobs to start containers:
* * * * * docker start systemdata
*/15 * * * * docker start networkdata

## Wakeonlan
sudo apt install wakeonlan
- Copy wake.sh
sudo chmod +x wake.sh
./wake.sh

!## Pihole
AFter setup, remove Google dns server from router configuration

!## Jellyfin
https://www.youtube.com/watch?v=HuHvSLX8JSQ

!## PiVPN

## Samba
Config:

[shared]
path=/mnt/media/shared
writeable=Yes
create mask=0777
directory mask=0777
public=no