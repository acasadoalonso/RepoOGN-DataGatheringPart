#!/bin/bash
vcgencmd otp_dump | grep 17:
sudo umount /dev/sda1
sudo umount /dev/sda2
echo  "Make partition table type:  mktable msdos........."
sudo parted  /dev/sda 

echo  "Format partition table  ........."
sudo parted  /dev/sda <<EOF
mkpart primary fat32 0% 100M
mkpart primary ext4 100M 100%
print
quit
EOF
echo "Done it........."
sleep 15
sudo mkfs.vfat -n BOOT -F 32 /dev/sda1
sudo mkfs.ext4 /dev/sda2
sudo mkdir /mnt/target
sudo mount /dev/sda2 /mnt/target/
sudo mkdir /mnt/target/boot
sudo mount /dev/sda1 /mnt/target/boot/
sudo apt-get update; sudo apt-get -y upgrade ; sudo apt-get install rsync
sudo rsync -ax --progress / /boot /mnt/target
cd /mnt/target
sudo mount --bind /dev dev
sudo mount --bind /sys sys
sudo mount --bind /proc proc
sudo chroot /mnt/target <<EOF
rm /etc/ssh/ssh_host*
dpkg-reconfigure openssh-server 
exit
EOF
cd /mnt/target
sudo umount dev
sudo umount sys
sudo umount proc
sleep 5
df
sudo sed -i "s,root=/dev/mmcblk0p2,root=/dev/sda2," /mnt/target/boot/cmdline.txt
sudo sed -i "s,/dev/mmcblk0p,/dev/sda," /mnt/target/etc/fstab
cd ~
sudo umount /mnt/target/boot 
sudo umount /mnt/target

df
echo " All Done it........."
