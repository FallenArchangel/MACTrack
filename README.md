# MACTrack
Program used to track users using MAC addresses.

# How does it work?
- First you need to find the MAC address of your target. 
- While close to your target, scan for nearby mac addresses.
- Next, wait until your target changes location, or everyone else leaves.
- Scan for mac addresses again. 
- Only keep addresses that were present in both scans.
- Continue until only one mac address remains. This must be your targets mac address.
- Next you may run this program at any time to see if your target is in wifi range or not. 
- More functionality is coming soon. This is the very early stages of this program.

# Requirements
Wireless card capable of monitor mode. airmon-ng, airodump-ng, and tshark.
'''
sudo apt-get install aircrack-ng tshark
'''

# Instructions
- First open settings.conf and make sure you have the correct wireless card selected. wlan0 is used by default.  
- Now open Known.txt and add a list of names and corresponding mac addresses like the example.
- Next run the program and wait thirty seconds to one minute for it to scan.
- hen it's finished scanning it will give you a list of MAC addresses found. If any of them are in your database of known MACs, it will show the name.

# To-Do
[] Add entries to Known.txt from within the program.

[] Compare macs from two locations to find matches.
