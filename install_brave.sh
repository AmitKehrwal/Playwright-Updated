#!/bin/bash     

# Install curl
sudo apt install -y curl

# Download the Brave browser keyring
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://$

# Add Brave browser repository to sources.list.d
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] htt$

# Update package list
sudo apt update

# Install Brave browser
sudo apt install -y brave-browser