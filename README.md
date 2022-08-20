# loadshed

This program is for houses that suffer consistent power outages and have a tesla powerwall installed. The powerwall holds a limited amount of power, especially during the winter when the panels produce less power and more outages occur. When the power goes out, some devices in the home are necessary to keep on while others are not. 

It uses python modules I found on Github to interface with a home's smart plugs and other devices (Tuya & Kasa Devices are currently supported), windows, solaris and Linux computers, and a tesla powerwall. The program will constantly run on a computer and check the powerwall for power outages, which if it detects will then run the load shedding function. All tuya and kasa devices will be shut down as well and the computers listed in a text file. When the prgogram detects that the powerwall has reconnected to the grid all the shut down devices will be brought back up. 

Of the system libraries used in the program of particular note are the following:
 - os: used to execute shell commands such as shutdown remote desktops and servers
 - threading: used to create separate threads for monitoring and user interface
 - curses: allows for creation of a textual user interface in the terminal

The three libraries specific to the program functionality are: tesla_powerwall library, kasa library and tinytuya. These allow the program to interface with the tesla powerwall, kasa devices, and tuya devices. 

Both the tesla_powerwall and kasa libraries were simple to set up. 

The tinytuya had a more complicated setup. It requires creating a tuya developer account on iot.tuya.com and then a cloud project under the account.

The program assumes that the following is done to prepare solaris and linux devices:
 - On the monitoring computer the ssh-keygen command is run to generate ssh authentication keys
 - For each  target computer, the authentication keys are copied using the ssh-copyid command
 
To setup the windows computers:

1) Add a remote shutdown security policy:
run secpol.msc
in the program tree, open Security Settings > Local Policies > User rights Assignment
Find the entry Force shutdown from a remote system
Edit the entry, add the windows user account that will be used for shutdown (ex: nouknouk)

2) Add registry keys to disable UAC remote restrictions:
Run regedit.exe as Administrator
Find HKLM/SOFTWARE/Microsoft/Windows/CurrentVersion/Policies/System
Create a new registry DWORD(32) value named LocalAccountTokenFilterPolicy and then assign it the value 1

3) Start remote registry service:
Open cmd.exeas Administrator
Execute the two following commands:
sc config RemoteRegistry start= auto
sc start RemoteRegistry

The following need to be configured in monitor.py for the program to work in your installation 

-powerwall name 
PWIPNAME = "XX.XX.XX.XX"

-powerwall password
PWPASS = "XXXXX"

-email to notify of grid changes and succesfull completion of program operations
In this case the email used will cause a text message to be sent to a mobile phone. 
tmomail.net is for T-Mobile customers. Find the equivalent email address if you are using a different cell provider).  
MAILNOTIF = "XXXXXXXXXX@tmomail.net"

-Tuya  credentials
TUYAAPIREGION="us"
TUYAAPIKEY="XXXXXXXXXXXXXXXXXXXX"
TUYAAPISECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TUYAAPIDEVICEID="XXXXXXXXXXXXXXXXXXXX"


links to libraries used:
 - Tesla Powerwall https://github.com/jrester/tesla_powerwall.
 - Tuya Devices: https://github.com/jasonacox/tinytuya
 - Kasa Devices: https://github.com/python-kasa/python-kasa
