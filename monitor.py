
# imported libraries

# time support
import time
import datetime

# execute shell commands
import os

# curses support interface
import curses
# multithreading support
import threading

# interface with powerwall see https://github.com/jasonacox/pypowerwall
import tesla_powerwall
from tesla_powerwall import Powerwall
from tesla_powerwall import User

# interface with kasa devices see https://github.com/python-kasa/python-kasa
import asyncio
from kasa import Discover

# interface with tuya devices see https://github.com/jasonacox/tinytuya
import tinytuya

# user modifiable variables
# location of directory with configuration files
FILEPATH = './'

# powerwall name 
PWIPNAME = "XX.XX.XX.XX"
# powerwall password
PWPASS = "XXXXX"
# email to notify of grid changes and succesfull completion of program operations
# in this case the email used will cause a text message to be sent to the customer mobile phone
MAILNOTIF = "XXXXXXXXXX@tmomail.net"
# Tuya  credentials
TUYAAPIREGION="us"
TUYAAPIKEY="XXXXXXXXXXXXXXXXXXXX"
TUYAAPISECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TUYAAPIDEVICEID="XXXXXXXXXXXXXXXXXXXX"

# main variables
# how often grid is checked in seconds
polltime = 300
#how long to wait before action is taken after grid change
confirmtime = 600

# comtrol whether debug prints are enabled or not
debug = False

# shut down windows computers
def windowshutdown():
        # read computer information file
        with open(FILEPATH + 'windows.txt') as f:
                lines = f.read().splitlines()
        # shut down each computer
        for line in lines:
                words = line.split()
                computername = words[0]
                username = words[1]
                password = words[2]
                monitorWindow.addstr('shutting down windows computer: ' + computername + '\n')
                command = 'net rpc -S ' + computername + ' -U ' + username + '%' + password + ' shutdown -t 1 -f'
                # depug print
                if (debug):
                        monitorWindow.addstr(command + '\n')
                monitorWindow.refresh()
                os.system(command)

# shutdown linux and solaris servers
def unixshutdown():
        # read server information file
        with open(FILEPATH + 'servers.txt') as f:
                lines = f.read().splitlines()
        # shut down each computer
        for line in lines:
                words = line.split()
                computertype = words[0]
                computername = words[1]
                monitorWindow.addstr('shutting down server computer: ' + computername + '\n')
                if (computertype ==  'S'):
                        command = 'ssh root@' + computername  + ' shutdown -y -i 5'
                elif (computertype == 'L'):
                        command = 'ssh root@' + computername + ' shutdown now'
                else:
                        command = ''
                        monitorWindow.addstr("Unknown server type:" +  computertype + '\n')
                # debug print
                if (debug):
                        monitorWindow.addstr(command + '\n')
                monitorWindow.refresh()
                os.system(command)
        time.sleep(120)
        pass

# shutdown kasa devices
def kasashutdown():
        # discover devices in local network
        devices = asyncio.run(Discover.discover())
        # shut down wach device
        for addr, dev in devices.items():
                monitorWindow.addstr('shutting down kasa device: ' + dev.model + ' ' + addr + '\n')
                monitorWindow.refresh()
                asyncio.run(dev.turn_off())

# bring up kasa devices
def kasabringup():
        # discover devices in local network
        devices = asyncio.run(Discover.discover())
        # bring up wach device
        for addr, dev in devices.items():
                monitorWindow.addstr('bringing up kasa device: ' + dev.model + ' ' + addr + '\n')
                monitorWindow.refresh()
                asyncio.run(dev.turn_on())

#shutdowm tuya devices
def tuyashutdown():
        localDevices = tinytuya.deviceScan()
        for element in localDevices:
                monitorWindow.addstr("shutting down tuya device: %r" % localDevices[element]['name'] + '\n')
                monitorWindow.refresh()
                dev = tinytuya.OutletDevice(localDevices[element]['gwId'], localDevices[element]['ip'], localDevices[element]['key'])
                dev.set_version(float(localDevices[element]['version']))
                dev.turn_off()

"""
        # create connection to tuya cloud
        c = tinytuya.Cloud(
                apiRegion = TUYAAPIREGION, 
                apiKey = TUYAAPIKEY, 
                apiSecret = TUYAAPISECRET, 
                apiDeviceID = TUYAAPIDEVICEID)

        # command to shutdowm switches
        switchoffcommand = {
                'commands': [{
                        'code': 'switch_1',
                        'value': False
                }, {
                        'code': 'countdown_1',
                        'value': 0
                }]
        }
        # command to shutdowm bulbs
        bulboffcommand = {
                'commands': [{
                        'code': 'switch_led',
                        'value': False
                }, {
                        'code': 'countdown_1',
                        'value': 0
                }]
        }
        # discover devices
        devices = c.getdevices()
        # shut down each device
        for element in devices:
                monitorWindow.addstr("shutting down tuya device: %r" % element["id"] + '\n')
                c.sendcommand(element["id"],switchoffcommand)
                c.sendcommand(element["id"],bulboffcommand)
                monitorWindow.refresh()
"""

# bring up tuya devices
def tuyabringup():
        localDevices = tinytuya.deviceScan()
        for element in localDevices:
                monitorWindow.addstr("bringing up tuya device: %r" % localDevices[element]['name'] + '\n')
                monitorWindow.refresh()
                dev = tinytuya.OutletDevice(localDevices[element]['gwId'], localDevices[element]['ip'], localDevices[element]['key'])
                dev.set_version(float(localDevices[element]['version']))
                dev.turn_on()
"""
        #cloud version
        # create connection to tuya cloud
        c = tinytuya.Cloud(
        apiRegion = TUYAAPIREGION, 
                apiKey = TUYAAPIKEY, 
                apiSecret = TUYAAPISECRET, 
                apiDeviceID = TUYAAPIDEVICEID)

        # command to bring up switches
        switchoncommand = {
                'commands': [{
                        'code': 'switch_1',
                        'value': True
                }, {
                        'code': 'countdown_1',
                        'value': 0
                }]
        }
        #command to bring up bulbs
        bulboncommand = {
                'commands': [{
                        'code': 'switch_led',
                        'value': True
                }, {
                        'code': 'countdown_1',
                        'value': 0
                }]
        }
        # discover devices
        devices = c.getdevices()
        for element in devices:
                monitorWindow.addstr("bringing up tuya device: %r" % element["id"] + '\n')
                c.sendcommand(element["id"],switchoncommand)
                c.sendcommand(element["id"],bulboncommand)
                monitorWindow.refresh()
"""

# main shutdown function
def shutdown():
        windowshutdown()
        unixshutdown()
        tuyashutdown()
        kasashutdown()
        # notify user
        os.system('mail -s "Grid is down, load has been shed"  ' + MAILNOTIF + ' < /dev/null') 
        monitorWindow.addstr('\n')
        monitorWindow.refresh()

# main bring up function
def bringup():
        kasabringup()
        tuyabringup()
        # notify user
        os.system('mail -s "Grid is up, load has been restored"  ' + MAILNOTIF + ' < /dev/null') 
        monitorWindow.addstr('\n')
        monitorWindow.refresh()


# grid status query function
def grid_down():
        # connect with powerwall
        powerwall=Powerwall(PWIPNAME)
        powerwall.login(PWPASS)
        status = powerwall.get_grid_status()
        time.sleep(polltime/10)
        meters = powerwall.get_meters()
        sitePower = meters.load.get_power()
        commandWindow.addstr(2,0,'powerwall charge (percentage): ' + format(powerwall.get_charge()) +'\n')
        monitorWindow.addstr(format(datetime.datetime.now()) + ' : ' + format(status) + ' ' + format(sitePower) + 'KW \n')
        monitorWindow.refresh()
        commandWindow.refresh()
        if (format(powerwall.get_grid_status()) == 'GridStatus.ISLANEDED'):
                powerwall.close()
                return True
        else:
                powerwall.close()
                return False

# main monitoring loop
def monitorloop():
        down = False
        while True:

                # loop while grid is up
                while not(grid_down()):
                        monitorWindow.addstr("up\n")
                        monitorWindow.refresh()
                        time.sleep(polltime)
                # grid is shut down
                else:
                        time.sleep(confirmtime)
                        if grid_down():
                                shutdown()
                                down = True
                                monitorWindow.addstr("down\n")
                                monitorWindow.refresh()
                if down:
                        # loop while grid is down
                        while grid_down():
                                monitorWindow.addstr("still down\n")
                                monitorWindow.refresh()
                                time.sleep(polltime)
                                # other programs may bring these devices up; make sure they stay down
                                tuyashutdown()
                                kasashutdown()
                        # grid came back up
                        else:
                                time.sleep(confirmtime)
                                if not(grid_down()):
                                        bringup()
                                        down = False
                                        monitorWindow.addstr("came up\n")
                                        monitorWindow.refresh()

# class to lanuch monitor thread
class monitorThread (threading.Thread):
        def run(self):
                monitorloop()

# user menu in the terminal
def menu():
        # present options
        commandWindow.addstr('__________________\n')
        commandWindow.addstr('1. Test Shutdown\n')
        commandWindow.addstr('2. Test Bringup\n')
        commandWindow.addstr('3. Exit program\n')
        commandWindow.addstr('__________________\n')
        commandWindow.refresh()
        # read input
        while (True):
                pass
                ch = commandWindow.getch()
                if (ch == ord('3')):
                        return()
                elif (ch == ord('2')):
                        monitorWindow.addstr('testing bringup \n')
                        monitorWindow.refresh()
                        bringup()
                elif (ch == ord('1')):
                        monitorWindow.addstr('testing shutdown \n')
                        monitorWindow.refresh()
                        shutdown()
                else:
                        pass

import threading, sys, traceback

def dumpstacks(signal, frame):
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    print("\n".join(code))

import signal

signal.signal(signal.SIGQUIT, dumpstacks)

# main body
if __name__ == '__main__':
        # initialze curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        
        #create monitor and command windows
        monitorWindow = curses.newwin(int(curses.LINES/2), curses.COLS, 0,0) 
        monitorWindow.scrollok(True)
        commandWindow = curses.newwin(int(curses.LINES/4), curses.COLS, 3*int(curses.LINES/4),0) 
        commandWindow.scrollok(False)

        
        # connect with powerwall
        pw=Powerwall(PWIPNAME)
        pw.login(PWPASS)
        # printing startup information in scrolling window
        monitorWindow.addstr('Powerwall monitoring is starting\n')
        monitorWindow.addstr(format(pw.get_grid_status()) + '\n')
        monitorWindow.refresh()
        
        # present powerwall information
        commandWindow.addstr('Powerwall: ' + PWIPNAME + '\n') 
        commandWindow.addstr('powerwall capacity (watts): ' + format(pw.get_capacity()) + '\n')
        commandWindow.addstr('\n')
        commandWindow.refresh()
        pw.close()
        
        # lauch monitor thread
        t = monitorThread(daemon=True)
        t.start()

        # call menu function
        menu()

        # restore terminal settings
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
