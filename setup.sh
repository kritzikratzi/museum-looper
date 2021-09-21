# Step 1: 
# Add the pi user to the sudoers list. This allows us to run sudo commands 
# without asking for a password
# Here you might get prompted for the current password (usually it's `raspberry`)
sudo cp assets/010_pi-nopasswd /etc/sudoers.d/010_pi-nopasswd

# Step 2: 
# The raspi-config ui will open up. 
# Navigate to `interfaces`, then `ssh` and enable it. 
# After that select `finish`
echo "Please enable sshd..."
sleep 3
sudo raspi-config

# Step 3: 
# Change the password to something actually secret. 
# If you don't want to change the password, type `a, enter, b, enter`
echo "Please set the password for the pi user..."
sudo passwd pi

# Step 4: 
# If the system time is off, then you won't be able to update the packages. 
# This will prompt for the timezone and then sync time with the internet. 
sudo dpkg-reconfigure tzdata
sudo apt update

# Step 5: Install debian packages 
# Automatic, you have nothing to do here. 
sudo apt -y install git build-essential python3-dev libssh-4 unclutter xdotool udisks2 exfat-fuse exfat-utils libnotify-bin

# Step 6: Disable the toast notifications after unplugging usb drives
# Automatic, you have nothing to do here. 
gsettings set org.gnome.desktop.notifications show-banners false

# Step 7: Install python packages 
# Automatic, you have nothing to do here. 
pip3 install inotify
pip3 install gi

# Step 8: Compile the black backdrop
# Automatic, you have nothing to do here. 
cd blocker
./build.sh
cd ..

# Step 9: Update the alsa configuration (does this work on raspi3??)
# Automatic, you have nothing to do here. 
cp assets/asoundrc_single ~/.asoundrc

# Step 10: Install autostart script
# Automatic, you have nothing to do here. 
sudo cp assets/looper.desktop /etc/xdg/autostart/looper.desktop

# Step 11: Create the config file if it doesn't exist. 
# You will asked to edit the file and supply: 
# a. A unique ip address for this device
# b. Set the computer to be the master/slave
if [ ! -f /boot/looper.txt ]
then
	sudo mount -o remount,rw /boot
	sudo cp assets/looper.txt /boot/looper.txt
	sudo nano /boot/looper.txt
fi

# Step 12: Disable dhcpcd
# Automatic, you have nothing to do here. 
# This will disable all automatic internet configuration (we don't need internet anymore)
systemctl disable dhcpcd
