sleep 5

cd /home/pi/SDP-Group-4
git pull

bash -c 'ifconfig -a > /home/pi/SDP-Group-4/NetworkLog.log 2>&1'

git add --all

git commit --all --message "pi boot"

git push
