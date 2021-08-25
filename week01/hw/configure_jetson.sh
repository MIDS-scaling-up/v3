#!/bin/sh

# Add user to docker group to avoid sudo
sudo usermod -aG docker $USER

# Turn of zram swap
sudo mv /etc/systemd/nvzramconfig.sh /etc/systemd/nvzramconfig.sh.save

# Create and enable a 32 GB swap space
sudo mkdir /data
sudo fallocate -l 36G /data/swapfile
sudo chmod 600 /data/swapfile
sudo mkswap /data/swapfile
sudo swapon /data/swapfile
sudo swapon -s
echo "/data/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab

