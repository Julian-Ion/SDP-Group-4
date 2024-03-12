#!/bin/bash

sleep 5

while ! ping -c 4 google.com > /dev/null; 
do 
echo "The network is not up yet"
sleep 1 
done

echo "Connected to network"

sudo git config --global --add safe.directory /home/pi/SDP-Group-4

cd /home/pi/SDP-Group-4
git pull

echo "Pull success"

bash -c 'ifconfig -a > /home/pi/SDP-Group-4/NetworkLog.log 2>&1'

git add --all

git commit --all --message "pi boot"

git push

echo "Push success"
