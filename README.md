The pi pulls the repo at boot, any commited changes will be updated on the pi when rebooted or turned on

startup.sh runs when the pi boots add anything extra that needs to happen at boot in there

pi pushes a file "NetworkLog.log" at boot which contains the IP address for the pi for SSH

command to ssh is "ssh pi@<IP>"

pi has the password "alfred"

pi should be able to connect to either eduroam or hotspot with name "testnet" and password "testnet1"
