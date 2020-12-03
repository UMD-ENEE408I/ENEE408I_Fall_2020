# Introdution

Setting up a remote desktop service on the Jetson is not as straightforward as it should be (single click in a settings GUI). Additionally, the instructions in the L4T-README/README-vnc.txt do not work as stated. The following worked on my Nano and should work on the Xavier NX.

# First run a bunch of commands to setup the VNC server

Note: "thepassword" is the vncserver password, it does not need to be the user accounts password

```bash
sudo apt update
sudo apt install vino

mkdir -p ~/.config/autostart
cp /usr/share/applications/vino-server.desktop ~/.config/autostart

gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false

gsettings set org.gnome.Vino authentication-methods "['vnc']"
gsettings set org.gnome.Vino vnc-password $(echo -n 'thepassword'|base64)
```

Edit the X11 configuration to add a high-resolution screen when there is no screen connected

Note: Else the default is 640x480. This will hard code your resolution even when connected with a monitor.

```bash
sudo gedit /etc/X11/xorg.conf
```

Add the following lines at the bottom, save and exit.

```
Section "Screen"
    Identifier "Default Screen"
    Monitor "Configured Monitor"
    Device "Tegra0"
    SubSection "Display"
        Depth 24
        Virtual 1920 1080 # Modify the resolution by editing these values
    EndSubSection
EndSection
```

# The auto-login instructions below do not seem to work on the Xavier NX
Some students have been able to enable it with the Settings GUI. Some have not.
Levi will debug it more once he gets a Xavier.
Enable auto-login so that the VNC server is started on power-up

~~Note: I also tried a systemd service, however it started the VNC server too early and it was not able to access the screen, causing a crash. This way is much easier to configure.~~

```bash
sudo gedit /etc/gdm3/custom.conf
```
Uncommented the following lines under the section [daemon], put your name on computer where "name" is , make sure 't' in 'true' is not capitalized, save and exit.

```
AutomaticLoginEnable=true
AutomaticLogin="name"
```

Make sure the following line is uncommented:

```
WaylandEnable=false
```

Get the Jetson's IP Address on your local network

```bash
ifconfig
```

Note the entry next to "inet" under the "wlan0" device.
My entry is: `192.168.1.72`

You can test if you have the correct ip address by opening a terminal on your PC that you will connect from and running `ping 192.168.1.72`. This should work on Windows, Linux, and OSX.

Reboot your Jetson and disconnect the screen

# Install a VNC Viewer on your PC

For Windows users, I recommend TightVNC: https://www.tightvnc.com/ (Links to an external site.)
You can select "Custom Installation" during setup to disable installation of a VNC server on your Windows PC.

I tried a couple other viewers on Windows and TightVNC seemed to be the best.

For MAC's, I am not sure what VNC software is best, though Google finds several options. Let us know what works!
Alvin used https://www.realvnc.com/en/connect/download/viewer/macos/ and it worked for him. 

After installing, run TightVNC and enter the ip address before in the "Remote Host" section, push connect, enter "thepassword" for the password, and you should be good to go.

# Bonus: SSH Access

You can also use this ip address for connecting over ssh (with Putty). Your username and password in this case will be your username and password for the Linux account.

# A Note on IP Addresses

This guide assumes your Jetson and PC are on the same local network. Your Jetson was auto-assigned an IP address by the router managing the network. It is possible for this address to change. Though somewhat unlikely unless the router is rebooted or a lot of devices connect to your router while the Jetson is not.

Some router's allow you to to assign static DHCP leases to clients. This would prevent the issue. Another is to manually configure the Jetson to use a static IP address within the allowable static IP address range for your local network, this is complicated and I wouldn't recommend it for this class.
