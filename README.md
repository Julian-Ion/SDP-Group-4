The pi pulls the repo at boot, any commited changes will be updated on the pi when rebooted or turned on

startup.sh runs when the pi boots add anything extra that needs to happen at boot in there

pi pushes a file "NetworkLog.log" at boot which contains the IP address for the pi for SSH

command to ssh is "ssh pi@<IP>"

pi has the password "alfred"

pi should be able to connect to either eduroam or hotspot with name "testnet" and password "testnet1"

Please try not to delete files on the pi directly it can mess stuff up

if you create or edit files directly on the pi make sure theyre in the /home/pi/SDP-Group-4 directory and then run "bash push.sh" on the terminal in the same directory to sych to this repo

if you don't run bash push.sh they wont be synched, but they won't be deleted either (i think), they should sync on the next boot
