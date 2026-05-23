# Controlling Microban outside of your local network

To have fun controlling Microban from anywhere, you can set up a Wi-Fi hotspot on your phone and connect the robot to it. This way, you will be able to access the robot remotely as long as your phone has an internet connection.

Note that this method requires a 2.4GHz Wi-Fi hotspot, as the Raspberry Pi Zero 2W does not support 5GHz Wi-Fi. This can generally be set up in the Wi-Fi settings of your phone.


## Setting up the SD card

To connect to your Wi-Fi hotspot, you will need to create a file named `telephone.nmconnection` in the `/etc/NetworkManager/system-connections/` directory of the root filesystem of your SD card. To do this, connect to your SD card and use the following command, replacing `[PC_NAME]` with the name of your computer:

```
sudo nano /media/[PC_NAME]/rootfs/etc/NetworkManager/system-connections/telephone.nmconnection
```

Paste the following content into the file, replacing `[HOTSPOT_NAME]` and `[HOTSPOT_PASSWORD]` with the actual name and password of your Wi-Fi hotspot:

```
[connection]
id=Telephone
uuid=12345678-1234-1234-1234-123456789abc
type=wifi

[wifi]
mode=infrastructure
ssid=[HOTSPOT_NAME]

[wifi-security]
key-mgmt=wpa-psk
psk=[HOTSPOT_PASSWORD]

[ipv4]
method=auto

[ipv6]
addr-gen-mode=default
method=auto
```

Then, set the permissions of the file to 600 to ensure that it is only readable by the root user:

```
sudo chmod 600 /media/[PC_NAME]/rootfs/etc/NetworkManager/system-connections/telephone.nmconnection
```

Finally, safely eject the SD card from your computer and insert it into the robot. When you power on the robot, it should automatically connect to the specified Wi-Fi hotspot.


## Accessing the robot remotely

To control the robot remotely, you will need to update the SSH config to use the new Wi-Fi connection.
To do this, you can add the following entry to your `~/.ssh/config` file:

```
Host microban-ext
    HostName <IP_ADDRESS>
    User <USERNAME>
```

To find the IP address of your robot, you can check the connected devices on your phone's Wi-Fi settings or use a network scanning tool such as `nmap` or `arp-scan`. The user name is the one you set up when you first booted the robot (cf. [Installation Guide](install.md)).

Once the SSH config is updated, you can connect to the robot using the following command:

```
ssh microban-ext
```

And add `HOST=microban-ext` to the same commands you would normally use to control the robot locally, such as `make run` or `make battery`. You can also set the `HOST` environment variable globally in your terminal session to avoid having to specify it for each command:

```
export HOST=microban-ext
```