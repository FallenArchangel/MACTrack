import os
import subprocess
import time


def loadconfig(line):
    if os.path.isfile("settings.conf"):
        configfile = open("settings.conf").read().splitlines()
        return configfile[int(line) - 1].strip()
    else:
        print("settings.conf does not exist.")


# Opens 'Known.txt' to build known devices dictionary.
def readknown(filename="Known.txt"):
    privateknownmacs = {}
    with open(filename, "r") as cache:
        # read file into a list of lines
        lines = cache.readlines()
        # loop through lines
        for line in lines:
            # skip lines starting with "--".
            if not line.startswith("--"):
                line = line.strip().split(" ")
                # use first item in list for the key, join remaining list items
                # with ", " for the value.
                privateknownmacs[line[0]] = ", ".join(line[1:])

    return privateknownmacs


# Checks if MACs.txt exists.
# Calls getscannedmacs if it does.
def checkformacs():
    filename = "MACs.txt"
    if os.path.isfile(filename):
        return getscannedmacs()
    else:
        print("MACs.txt does not exist.")


# Reads every line from MACs.txt into a list.
# Makes variable 'macs' which contains a list without duplicates
def getscannedmacs():
    originalmacs = open("MACs.txt").read().splitlines()
    macs = list(set(originalmacs))
    return parsemacs(macs)


# Takes list of MACs and compares them to dictionary. Replaces with hostname if known.
def parsemacs(unparsedmacs):
    knownmacs = readknown()
    devicesinrange = []
    for x in range(0, len(unparsedmacs)):
        try:
            devicesinrange.append(knownmacs[unparsedmacs[x]])
        except KeyError:
            devicesinrange.append(unparsedmacs[x])
    devicesinrange.append(" ")
    devicesinrangestring = "\n".join(devicesinrange)
    return devicesinrangestring


def start():
    cmd = ['ifconfig']
    if subprocess.check_output(cmd).decode().find(loadconfig(3) + "mon") == -1:
        print(loadconfig(3) + "mon not found, launching airmon, waiting 30 seconds, and restarting")
        os.system("sudo airmon-ng start " + loadconfig(3))
        time.sleep(30)
        start()
    else:
        print(loadconfig(3) + "mon found, starting scan")
        return scan()


def scan():
    try:
        os.remove('MACs.txt')
    except OSError:
        pass
    os.system('tshark -Q -l -i ' + loadconfig(3) + 'mon -T fields -e wlan.sa -a duration:' + loadconfig(6) + ' |' +
              ' grep -ioE \'([a-z0-9]{2}:){5}..\' >> MACs.txt')
    return checkformacs()


try:
    print(start())
except TypeError:
    print("No devices found")
