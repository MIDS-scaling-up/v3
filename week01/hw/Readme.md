# HW 1: Installing JetPack and Docker 


## 1. Nvidia JetPack SDK
JetPack is an SDK that basically contains everything needed for deep learning and AI applications in a handy package bundle containing the OS for for the Nano. Installation on the Nano requires downloading and flashing the image to a MicroSD card.

Due to supply shortages, we are recommending the Jetson Nano Developer Kit 4GB model over the Jetson Xaiver NX Developer Kit.  If you are able to find an NX, feel free to use that instead of the Nano.


You will need the following:

 1. [Jetson Nano Developer Ki: ideally 4GB, but 2GB if that is all you can find](https://shop.nvidia.com/en-us/jetson/store/?page=1&limit=9&locale=en-us)
 2. [128GB Micro SD](https://www.amazon.com/gp/product/B07G3H5RBT/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
 3. USB MicroSD card reader
 4. [WiFi/Bluetooth card](https://www.amazon.com/dp/B085M7VPDP?psc=1&ref=ppx_yo2_dt_b_product_details)
 5. [Power adapter](https://www.amazon.com/gp/product/B08DXZ1MSY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) ### NOTE: ensure you set the jumper when using the power adapter. Reference [here](https://www.jetsonhacks.com/2019/04/10/jetson-nano-use-more-power/).  Note: if you are using [the Nano 2GB](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-2gb-devkit), check out the [list of supported components](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide#id-.JetsonNano2GBDeveloperKitUserGuidevbatuu_v1.0-SupportedComponentList).  You could get [this 3.5A power supply.](https://www.amazon.com/CanaKit-Raspberry-Power-Supply-USB-C/dp/B07TYQRXTK/ref=sr_1_8?dchild=1&keywords=18W+power+supply+usb+c&qid=1595554849&sr=8-8)
 6. [1TB USB3 SSD](https://www.amazon.com/Samsung-T5-Portable-SSD-MU-PA2T0B/dp/B073H552FJ/ref=sr_1_3) ### NOTE: mount to the normal USB port; the USB-C port is needed for the power supply.
 7. [USB Webcam](https://www.amazon.com/Logitech-960-000637-HD-Webcam-C310/dp/B003PAIV2Q/ref=sr_1_6)

If you are able to find a Jetson NX, the following is needed:
 1. MicroSD card (64GB minimum size)
 2. USB MicroSD card reader
 3. NVMe M.2 SSD (256GB minimum size) **NOTE: SATA M.2 SSDs will not work**
 4. Size 0 Philips head screwdriver
 5. Micro USB to USB cable
 6. USB Webcam

### 1.1 Host (Computer) Installation

On your Windows, Mac, or Ubuntu workstation, navigate to the [JetPack homepage](https://developer.nvidia.com/jetpack) (**NOTE that we are using JetPack 4.6 for this class**) and click on "Download SD Card Image" in the `JETSON XAVIER NX DEVELOPER KIT` box. Once it downloads, follow the steps at [Getting Started with Jetson Xavier NX Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit) to flash the SD card.

NVIDIA provides [flashing instructions](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write) for Windows, Linux, and Mac. You will need to insert the MicroSD card into the card reader and connect it to the USB port on your computer.


A quick video showing MicroSD card [here](Xavier_NX_Install_SSD.mp4). Note, this video is for a Jetson Xavier NX and includes the installation of a SSD.

Once the flashing process is complete, you will insert the MicroSD card into your Jetson. **Do not power it on yet.**




### 1.2 Post-flash setup

There are two setup options. 

 1. Use a USB keyboard/mouse and HDMI display
 2. Use a tty terminal from Mac or Linux

With the first option, you will obviously need additional hardware. Option number two is quite easy, though, and we will walk you through the process.

If you choose option two, you will need a machine running Linux (we recommend Ubuntu 18.04), or a Mac. If you do not have one, you can create a VM running Ubuntu (see section 1.2).

If you are using install option one, you can connect the keyboard, mouse, and display to [complete the setup process](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup). Once they are connected, you can connect the power adapter. Follow the steps to complete the setup and then go to section 2. If you have issues connecting to wifi, skip that step and connect the Nano directly to your router with an ethernet cable **after** the setup is complete.

If you are using install option two, you can connect the Nano to your Mac or Linux computer using the micro-USB cable and then connect the power adapter.

**If you are using a VMware VM, you will be prompted to connect the USB device to your host computer or the VM; choose the VM. When in the VM, use "lsusb" in the terminal to check if the Jetson is visible.**

### 1.3 If you chose Option 2 in section 1.2

You will need to use a Linux VM or a Mac to perform these steps.

#### 1.3.1 Create a VM (skip this step if you are using a Mac)

You get a free VMware subscription through Berkeley [here](https://software.berkeley.edu/vmware). Download and install VMware Workstation (for Windows) or VMware Fusion (for macOS).

Download the Ubuntu 18.04 iso image [here](http://releases.ubuntu.com/18.04/ubuntu-18.04.3-desktop-amd64.iso). 

Create a new VM in VMware. 

Walk-through on VMware image creation is [here](CreateUbuntuVMInVMware.mp4).

**VM Configuration**, the size of the disk should be 40GB absolutely minimum. Give the VM 2-4 cores to make sure cross-compilation does not take forever, and at least 4-8G of RAM. 


#### 1.3.2 Mac: 
Run this command from the Mac Terminal application:

```
ls -ls /dev/cu.*
```

You should see a `usbmodem` device like:

```
/dev/cu.usbmodem14210200096973
```

You will use the `screen` command to connect to the tty device:

```
screen /dev/cu.usbmode* 115200 -L
```

#### 1.3.3 Linux:
Run this command from the Linux terminal application:

```
ls -ls /dev/ttyA*
```

You should see a `ttyACM` device like:

```
/dev/ttyACM0
```
You will use the `screen` command to connect to the tty device:

```
sudo apt-get update
sudo apt-get install -y screen
sudo screen /dev/ttyACM0 115200 -L
```

### 1.4 Both Linux and Mac:

You will finish the [setup process](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup) using the tty terminal you just opened to the device. 

## 2. Configure VNC

It is highly recommended that you connect your Nano directly to your router with an ethernet cable.

You can have a keyboard, mouse, and monitor attached to your Jetson; but it is also extremely convenient to set up screen sharing, so you can see the Jetson desktop remotely. This is needed, for instance, when you want to show Jetson's screen over a web conference - plus it's a lot easier than switching between monitors all the time.

1.  Get a VNC screen sharing client.  You can install [TightVNC](https://www.tightvnc.com/), [Remmina](https://remmina.org/), or another VNC client of your choice. 
2. Configure your Nano for remote screen sharing.

On your Nano, open a terminal (or ssh to your Nano from another computer). 

```
mkdir ~/.config/autostart
```
* Now, create/open the file ```~/.config/autostart/vino-server.desktop``` and insert the following:

```
[Desktop Entry]
Type=Application
Name=Vino VNC server
Exec=/usr/lib/vino/vino-server
NoDisplay=true
```

* Disable security by running the following from the command line:

```
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
```

* Enable automatic login by editing /etc/gdm3/custom.conf and add the following (the AutomaticLogin ID should be the user ID you created in the setup):

```
# Enabling automatic login
  AutomaticLoginEnable = true
  AutomaticLogin = nvidia # Ensure that you replace 'nvidia' with the ID you use to login to your Nano
```


* Reboot your Nano
* Then, launch your remote sharing client, choose VNC as the protocol, type in the IP address of your jetson and port 5900.

**NOTE:**
To find your IP address, use the following command:

```
nvidia@nano:~$ ip addr show | grep inet
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
    inet 192.168.11.103/24 brd 192.168.11.255 scope global dynamic noprefixroute eth0
    inet6 fe80::4ab0:2dff:fe05:a700/64 scope link noprefixroute 
nvidia@nano:~$ 
```
The IP address in this example is on the third line: `192.168.11.103`.

When using VNC it is strongly recommended to us a reslution less than 4k as resolutions at 4k or higher can cause additional lag.
For example, a resolution of 1600x900 typically decent performance (you may adjust as needed).

Make sure your display cable is not plugged into your Nano (if it is, unplug it and reboot) and from a SSH shell enter: 
```
export DISPLAY=:0
xhost +
sudo xrandr --fb 1600x900
```

You'll need to run this after you reboot your Nano.

### Now run a VNC viewer on your computer (not the Jetson):

On any platform, you can download a VNC Viewer (like Real VNC) and use it: 

![vnc2](vnc2.png)
and

![vnc1](vnc1.png)

On Linux, you can use Remmina: 

![remmina](remmina2.png)

* The default resolution is very small. You can change it with this command (required after every reboot):

```
sudo xrandr --fb 1600x900 # you can choose some other resolution if desired
```




### Testing JetPack on the Nano
Ensure the Nano is on and running Ubuntu. Use this command to verify that everything is happy and healthy:

```
sudo nvpmodel -q --verbose
```

The output should be similar to:

```
NVPM VERB: Config file: /etc/nvpmodel.conf
NVPM VERB: parsing done for /etc/nvpmodel.conf
NVPM WARN: fan mode is not set!
NVPM VERB: Current mode: NV Power Mode: MAXN
0
NVPM VERB: PARAM CPU_ONLINE: ARG CORE_0: PATH /sys/devices/system/cpu/cpu0/online: REAL_VAL: 1 CONF_VAL: 1
NVPM VERB: PARAM CPU_ONLINE: ARG CORE_1: PATH /sys/devices/system/cpu/cpu1/online: REAL_VAL: 1 CONF_VAL: 1
NVPM VERB: PARAM CPU_ONLINE: ARG CORE_2: PATH /sys/devices/system/cpu/cpu2/online: REAL_VAL: 1 CONF_VAL: 1
NVPM VERB: PARAM CPU_ONLINE: ARG CORE_3: PATH /sys/devices/system/cpu/cpu3/online: REAL_VAL: 1 CONF_VAL: 1
NVPM VERB: PARAM CPU_A57: ARG MIN_FREQ: PATH /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq: REAL_VAL: 102000 CONF_VAL: 0
NVPM VERB: PARAM CPU_A57: ARG MAX_FREQ: PATH /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: REAL_VAL: 1479000 CONF_VAL: 2147483647
NVPM VERB: PARAM GPU_POWER_CONTROL_ENABLE: ARG GPU_PWR_CNTL_EN: PATH /sys/devices/gpu.0/power/control: REAL_VAL: auto CONF_VAL: on
NVPM VERB: PARAM GPU: ARG MIN_FREQ: PATH /sys/devices/gpu.0/devfreq/57000000.gpu/min_freq: REAL_VAL: 76800000 CONF_VAL: 0
NVPM VERB: PARAM GPU: ARG MAX_FREQ: PATH /sys/devices/gpu.0/devfreq/57000000.gpu/max_freq: REAL_VAL: 921600000 CONF_VAL: 2147483647
NVPM VERB: PARAM GPU_POWER_CONTROL_DISABLE: ARG GPU_PWR_CNTL_DIS: PATH /sys/devices/gpu.0/power/control: REAL_VAL: auto CONF_VAL: auto
NVPM VERB: PARAM EMC: ARG MAX_FREQ: PATH /sys/kernel/nvpmodel_emc_cap/emc_iso_cap: REAL_VAL: 0 CONF_VAL: 0
NVPM VERB: PARAM CVNAS: ARG MAX_FREQ: PATH /sys/kernel/nvpmodel_emc_cap/nafll_cvnas: REAL_VAL: 576000000 CONF_VAL: 576000000

```

### Exploring the power modes of the Nano
The Jetson line of SoCs (including the Nano) has a number of different power modes described in some detail here: [TX2](https://www.jetsonhacks.com/2017/03/25/nvpmodel-nvidia-jetson-tx2-development-kit/) or [Xavier](https://www.jetsonhacks.com/2018/10/07/nvpmodel-nvidia-jetson-agx-xavier-developer-kit/). The main idea is that the lowering clock speeds on the cpu and turning off cores saves energy; and the default power mode is a low energy mode. You need to switch to a higher power mode to use all cores and maximize the clock frequency.  In the upper right corner of your desktop you will see a widget that should allow you to switch between power modes.  Set your power mode to MAXN; this will enable all  cores and will maximize your clock frequency. This is ok when we use our Nano as a small desktop computer.  If you decide to use your Nano as a robotic device and become worried about the power draw, you may want to lower this setting.

## 3. Prepare the SSD

### 3.1 Configure a USB-attached SSD (both Nano and Xavier)
### Note: If you have a NVMe SSD on your Xavier, skip to section 3.2

Run `lsblk` to find the SSD. 

The output will show all your block devices. Look under the SIZE column for the correct size device (465.8G in the example below). Note the device name (sda in the example below). Your output should show a / in the MOUNTPOINT column of the mmcblk0p1 line:

```
NAME         MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop0          7:0    0    16M  1 loop 
sda            8:0    0 465.8G  0 disk 
mtdblock0     31:0    0    32M  0 disk 
mmcblk0      179:0    0  59.5G  0 disk 
├─mmcblk0p1  179:1    0  59.2G  0 part /
├─mmcblk0p2  179:2    0    64M  0 part 
├─mmcblk0p3  179:3    0    64M  0 part 
├─mmcblk0p4  179:4    0   448K  0 part 
├─mmcblk0p5  179:5    0   448K  0 part 
├─mmcblk0p6  179:6    0    63M  0 part 
├─mmcblk0p7  179:7    0   512K  0 part 
├─mmcblk0p8  179:8    0   256K  0 part 
├─mmcblk0p9  179:9    0   256K  0 part 
├─mmcblk0p10 179:10   0   100M  0 part 
└─mmcblk0p11 179:11   0    18K  0 part 
zram0        252:0    0 494.5M  0 disk [SWAP]
zram1        252:1    0 494.5M  0 disk [SWAP]
zram2        252:2    0 494.5M  0 disk [SWAP]
zram3        252:3    0 494.5M  0 disk [SWAP]
```

To setup the SSD, run the following commands:

```
# Wipe the SSD
sudo wipefs --all --force /dev/sda

# Partition the SSD 
sudo parted --script /dev/sda mklabel gpt mkpart primary ext4 0% 100%

# Format the newly created partition
sudo mkfs.ext4 /dev/sda1

# Create the fstab entry
echo "/dev/sda1 /data ext4 defaults 0 1" | sudo tee -a /etc/fstab

# Mount the ssd and set the permissions
mkdir /data
mount /data
chmod go+rwx /data

# Move the Docker repo to /data
sudo systemctl start docker
sudo mv /var/lib/docker /data/
sudo ln -s /data/docker/ /var/lib/docker
sudo systemctl start docker

# Verify that Docker re-started
sudo systemctl status docker

```

Continue to section 3.3 to set up the swap space.

### 3.2 Configure Operating System to run from SSD (Xavier NX with a NVMe ONLY)

### Note: It is advised to run lsblk after each reboot to ensure that the Jetson is using the correct boot device.

Steps:

### Note, with 4.6, there may be times when the Jetson fails to use the attached SSD as the root file system.  You can check this by running `lsblk` and confirmning the SD card is not using / as a mount point.  A reboot seems to correct this.


Follow the instructions on [this page](https://www.jetsonhacks.com/2020/05/29/jetson-xavier-nx-run-from-ssd/) (watch the video carefully).

# WARNING: This is a destructive process and will wipe your SSD. 
### Note: This version is for an Xavier NX with a NVMe SSD located at /dev/nvme0n1, which is the standard device location

Steps:

Verify that the OS is booting from the Micro SD.

```
lsblk
```

Your output should show a `/` in the MOUNTPOINT column of the `mmcblk0p1` line:

```
NAME         MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop0          7:0    0    16M  1 loop 
mtdblock0     31:0    0    32M  0 disk 
mmcblk0      179:0    0  59.5G  0 disk 
├─mmcblk0p1  179:1    0  59.2G  0 part /
├─mmcblk0p2  179:2    0    64M  0 part 
├─mmcblk0p3  179:3    0    64M  0 part 
├─mmcblk0p4  179:4    0   448K  0 part 
├─mmcblk0p5  179:5    0   448K  0 part 
├─mmcblk0p6  179:6    0    63M  0 part 
├─mmcblk0p7  179:7    0   512K  0 part 
├─mmcblk0p8  179:8    0   256K  0 part 
├─mmcblk0p9  179:9    0   256K  0 part 
├─mmcblk0p10 179:10   0   100M  0 part 
└─mmcblk0p11 179:11   0    18K  0 part 
zram0        252:0    0   1.9G  0 disk [SWAP]
zram1        252:1    0   1.9G  0 disk [SWAP]
nvme0n1      259:0    0 465.8G  0 disk 
```

To setup the SSD:

```
# Wipe the SSD
sudo wipefs --all --force /dev/nvme0n1

# Partition the SSD 
sudo parted --script /dev/nvme0n1 mklabel gpt mkpart primary ext4 0% 100%

# Format the newly created partition
sudo mkfs.ext4 /dev/nvme0n1p1

# We will use the jetsonhacks scripts to move data and enable the SSD as
# the default disk

git clone https://github.com/jetsonhacks/rootOnNVMe.git
cd rootOnNVMe/
sudo ./copy-rootfs-ssd.sh
./setup-service.sh

# Reboot for the update to take effect
sudo reboot
```

Run the `lsblk` command again to verify that you are running the OS from the SSD. This time, the `/` should be the MOUNTPOINT for `nvme0n1p1`:


```
NAME         MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop0          7:0    0    16M  1 loop 
mtdblock0     31:0    0    32M  0 disk 
mmcblk0      179:0    0  59.5G  0 disk 
├─mmcblk0p1  179:1    0  59.2G  0 part /media/nvidia/48fc8f75-dc2b-4a68-9673-c4cc26f9d5db
├─mmcblk0p2  179:2    0    64M  0 part 
├─mmcblk0p3  179:3    0    64M  0 part 
├─mmcblk0p4  179:4    0   448K  0 part 
├─mmcblk0p5  179:5    0   448K  0 part 
├─mmcblk0p6  179:6    0    63M  0 part 
├─mmcblk0p7  179:7    0   512K  0 part 
├─mmcblk0p8  179:8    0   256K  0 part 
├─mmcblk0p9  179:9    0   256K  0 part 
├─mmcblk0p10 179:10   0   100M  0 part 
└─mmcblk0p11 179:11   0    18K  0 part 
zram0        252:0    0   1.9G  0 disk [SWAP]
zram1        252:1    0   1.9G  0 disk [SWAP]
nvme0n1      259:0    0 465.8G  0 disk 
└─nvme0n1p1  259:1    0 465.8G  0 part /
```

### 3.3 Set up swap (both Nano and Xavier)

Use the `configure_jetson.sh` script in this repo to set up swap space after you have rebooted and verified that you are running your Operating System from the SSD:

```
git clone https://github.com/MIDS-scaling-up/v3.git
cd v3/week01/hw
chmod +x configure_jetson.sh
./configure_jetson.sh
```

Install jtop (a monitoring tool from https://github.com/rbonghi/jetson_stats):

```
sudo apt update
sudo apt install -y python3-pip
sudo -H pip3 install -U jetson-stats
sudo reboot

# Test after reboot
jtop
```

  
## 4. Docker 
Docker is a platform that allows you to create, deploy, and run applications in containers. The application and all its dependecies are packaged into one container that is easy to ship out and uses the same Linux kernel as the system it's running on, unlike a virtual machine. This makes it especially useful for compact platforms such as the Jetson.

JetPack 4.3+ has Docker pre-installed, and has an experimental nvidia-docker support.

Let's test it to see if it can run containers. Since the Jetson doesn't have the docker image 'hello-world' downloaded yet, Docker will automatically pull it online from the official repository:

```
docker run hello-world
```

Note, if you get a permissions error, run this command:
```
sudo usermod -aG docker $USER
```
Log out and log back in so that your group membership is re-evaluated.

 
### Run the base Docker Image for the Jetson
Most of the work  in the class will require a Docker base image running Ubuntu 18.04 with all the needed dependencies. For the first time, in July 2019, Nvidia has released an officially supported base cuda container! Please register at the [Nvidia GPU Cloud](http://ngc.nvidia.com) and review the documentation for the [base jetson container](https://ngc.nvidia.com/catalog/containers/nvidia:l4t-base)

Let's start this container:

```
# allow remote X connections
xhost +
# assuming that r32.4.3 is the latest version; but please check the NGC
docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.4.4
# this should complete successfully. Run this command to verify that you are inside the Docker container

ls
# You should see the following:
# bin  boot  dev  dst  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

# Now exit from the container:
exit
```
More on the use of this container is [here](https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-Container-Runtime-on-Jetson)

Note that our own old Docker images for the Jetsons are still available in the [docker hub](https://cloud.docker.com/u/w251/), e.g.  ```w251/cuda:tx2-4.3_b132``` and ```w251/cuda:dev-tx2-4.3_b132```. As the officially supported containers mature, we expect to sunset these; but for now, we'll keep them around just in case. We keep Dockerfiles for all of our containers [here](https://github.com/MIDS-scaling-up/v2/tree/master/backup) for your reference.

We'll cover Docker during the in-class lab in more detail.


# To turn in
Please send a message on the class portal homework submission page indicating that you were able to set up your Jetson
