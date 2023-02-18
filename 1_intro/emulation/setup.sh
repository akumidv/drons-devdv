#!/bin/bash

# https://mavsdk.mavlink.io/main/en/python/quickstart.html
# https://docs.px4.io/main/en/simulation/jmavsim.html

cd dev_env_install
source ubuntu.sh
pip3 install -r requirements.txt
cd ..

git clone --recursive -j8 https://github.com/PX4/Firmware.git PX4_Firmware


sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install -y gz-garden

git clone --recursive -j8 https://github.com/PX4/Firmware.git PX4_Firmware_gazebo

docker pull jonasvautherin/px4-gazebo-headless:1.13.2


#git clone --recursive -j8 https://github.com/PX4/Firmware.git PX4_Firmware_jsbsim
#wget https://github.com/JSBSim-Team/jsbsim/releases/download/Linux/JSBSim-devel_1.2.0.dev1-1032.bionic.amd64.deb
#sudo dpkg -i JSBSim-devel_1.2.0.dev1-1032.bionic.amd64.deb


#git clone --recursive -j8 https://github.com/PX4/Firmware.git PX4_Firmware_flightgear
#sudo add-apt-repository ppa:saiarcot895/flightgear
#sudo apt update
#sudo apt install -y flightgear

