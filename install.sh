#!/bin/bash

# Update and install necessary packages
sudo apt update
sudo apt install -y git tmux wget curl

# Clone the Waterwall Panel repository
git clone https://github.com/valizadeidin/Waterwall-Panel.git ~/Waterwall-Panel

# Download the latest release of WaterWall
WATERWALL_LATEST=$(curl -s https://api.github.com/repos/radkesvat/WaterWall/releases/latest | grep "tag_name" | awk '{print substr($2, 2, length($2)-3)}')
wget https://github.com/radkesvat/WaterWall/archive/refs/tags/$WATERWALL_LATEST.tar.gz -O ~/WaterWall-$WATERWALL_LATEST.tar.gz

# Extract the downloaded release
mkdir -p ~/WaterWall
tar -xzf ~/WaterWall-$WATERWALL_LATEST.tar.gz -C ~/WaterWall --strip-components=1

# Add WaterWall to PATH
echo 'export PATH=$PATH:~/WaterWall' >> ~/.bashrc
source ~/.bashrc

# Create a systemd service file for WaterWall
sudo bash -c 'cat <<EOF > /etc/systemd/system/waterwall.service
[Unit]
Description=WaterWall Service
[Service]
Type=oneshot
ExecStart=/usr/bin/tmux new-session -d -s "waterwall" ~/WaterWall/waterwall
ExecStop=/usr/bin/tmux kill-session -t waterwall
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd and enable the WaterWall service
sudo systemctl daemon-reload
sudo systemctl enable waterwall.service

# Start the WaterWall service
sudo systemctl start waterwall.service

echo "Installation and setup completed. WaterWall service is running."
