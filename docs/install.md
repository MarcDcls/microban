TODO before release: reflash en enlevant les info du wifi de Rhoban

## Step 1: Flash the Image

You can use Raspberry Pi Imager or the dd command line tool on Ubuntu to flash the custom .img file onto your micro-SD card.

TODO: add instructions for Raspberry Pi Imager

## Step 2: Headless Wi-Fi Configuration

Once the flashing process is complete, unplug and plug back the micro-SD card into your Ubuntu PC.

Open your terminal and open the network configuration file using nano:

```bash
sudo nano /media/$USER/bootfs/network-config
```

You should see a YAML file with the following content:

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      dhcp6: true
      optional: true
  wifis:
    wlan0:
      dhcp4: true
      regulatory-domain: "<YOUR_COUNTRY_CODE>"
      access-points:
        "<YOUR_WIFI_NAME>":
          password: "<YOUR_WIFI_PASSWORD>"
      optional: true
```

⚠️ CRITICAL: DO NOT modify the YAML format. It is strictly space-sensitive and should not be changed. 

🛜 Replace <YOUR_WIFI_NAME> and <YOUR_WIFI_PASSWORD> with your local network credentials. In addition, you can set other networks, such as your phone hotspot to use your robot everywhere. To do so, add an entry to the access-points section:

```yaml
      access-points:
        "<YOUR_WIFI_NAME>":
          password: "<YOUR_WIFI_PASSWORD>"
        "<YOUR_SECOND_WIFI_NAME>":
          password: "<YOUR_SECOND_WIFI_PASSWORD>"
```

🌍 Don't forget to replace <YOUR_COUNTRY_CODE> with your local two-letter country code (ISO 3166-1 alpha-2). For example, use "US" for the United States, "GB" for the United Kingdom, "FR" for France, "DE" for Germany, etc. This ensures the Raspberry Pi uses the correct Wi-Fi channels allowed in your country.

Save and exit (Ctrl + O, then Enter, then Ctrl + X).

Safely eject the card from your Ubuntu PC, insert it into the Raspberry Pi Zero 2W, and power it up.

## Step 3: First SSH Connection

Give the Raspberry Pi about 1 to 2 minutes on its very first boot. It will automatically resize the file system to use the full capacity of your SD card and then connect to your Wi-Fi network. Do not power it off during this process, as it may take a while and interrupting it could cause issues.

When the Pi is ready, you should be able to ping it from your computer using the command:

```bash
ping microban.local
```

You should see a response looking like this:
```
PING microban.local (192.168.XXX.XX) 56(84) bytes of data.
64 bytes from 192.168.XXX.XXX: icmp_seq=1 ttl=64 time=100 ms
...
```

The default credentials of this image are:
- Username: user
- Password: password

Open your terminal and run the following command:

```bash
ssh user@microban.local
```

TODO: finish the installation instruciton from there.

Username: <Insert_Your_Username_Here>

Password: <Insert_Your_Password_Here>

(Note: If microban.local cannot be found, look up your local router's DHCP client list to find the new IP address assigned to the Pi).

## Step 4: Personalize and Secure Your Robot
Once you are successfully connected via SSH, you should change the default password and customize the hostname.

1. Change the Password
Run the password tool and follow the on-screen prompts:

Bash
passwd
2. Change the Hostname (Robot Name)
If you want to rename your robot so it doesn't use microban on the network anymore, update the hostname:

Bash
sudo hostnamectl set-hostname NEW_ROBOT_NAME
Next, update the local hosts file to match the new name:

Bash
sudo nano /etc/hosts
Find the line containing microban (usually the second line) and replace it with your NEW_ROBOT_NAME. Save and exit (Ctrl+O, Enter, Ctrl+X).

Finally, apply all changes by rebooting the Pi:

Bash
sudo reboot
Your robot is now fully operational, secured, and discoverable at ssh <YOUR_USER>@NEW_ROBOT_NAME.local!