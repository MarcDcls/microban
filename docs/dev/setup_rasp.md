## Raspberry Pi setup

- Download the Raspberry Pi imager: https://www.raspberrypi.com/software/
- Plug your sd card in your computer
- Run it as sudo:

```
sudo Downloads/imager_[...].AppImage
```

- Select Raspberry Pi Zero 2 W
- Select Raspberry Pi OS (other)
- Select Raspberry Pi OS Lite (64-bit)
- Select your SD card
- Name it "microban"
- Select your timezone
- Set a username and a password
- Set the SSID and password of your local network (2.4 GHz)
- Activate SSH with password authentification
- Write

Once it's done, eject the SD card and plug it in your robot. It should boot and connect to your wifi. The first time it boots, it will take a while to expand the filesystem and install updates, so be patient and don't switch it off.

## Connecting to the Pi from your computer

To connect to your Raspberry Pi from your computer, it needs to be on the same network. 
Once on the same network, you can find the IP address of your Raspberry Pi by running:
```
ping microban.local
```

You should see a response looking like this:
```
64 bytes from 192.168.XXX.XXX: icmp_seq=1 ttl=64 time=100 ms
```

Then define a hostname for the Pi in your SSH config. To do this, add this entry to your `~/.ssh/config` file, with <USERNAME> being the username you set during the imager setup:
```
Host microban
    HostName 192.168.XXX.XXX
    User <USERNAME>
```

Finally, you can connect to the Pi with
```
ssh microban
```

In order not to have to enter the password everytime you connect to the Pi, you can copy your SSH key to the Pi. If you don't have an SSH key, you can generate one by running:
```
ssh-keygen -t ed25519
```

Then, copy your SSH key to the Pi with:
```
ssh-copy-id microban
```

Now you can connect to the Pi without entering a password!

## Raspberry Pi configuration

Copy the configuration file to the Pi. From your computer, run:
```
scp docs/dev/config.txt microban:config.txt
```

Then, on the Pi, move the configuration file to the correct location:
```
sudo mv config.txt /boot/firmware/config.txt
```

Reboot the Pi with `sudo reboot` for the changes to take effect.

After rebooting, connect to the Pi with `ssh microban` and setup the raspi-config:
- run `sudo raspi-config`
    - go to Interface Options
        - go to I2C
            - enable I2C    
        - go to Serial Port
            - disable Serial Console
            - enable Serial Port

Then, to prevent ssh hangs when the Pi is idle, run:
```
sudo nmcli con mod <tab_to_find_your_wifi_connection> wifi.powersave disable
```

Finally desactivate automatic updates by running 
```
sudo touch /etc/apt/apt.conf.d/99disable-auto-upgrades
cat << 'EOF' | sudo tee /etc/apt/apt.conf.d/99disable-auto-upgrades > /dev/null
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
APT::Periodic::Unattended-Upgrade "0";
EOF
```

Reboot the Pi with `sudo reboot`.
