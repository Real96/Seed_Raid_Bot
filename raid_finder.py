#Set game text speed to normal
#Save in front of a Den. You must have at least one Wishing Piece in your bag
#Start the bot with game closed and selection square over it
#isRare == 0/1 (search rare beam raid seeds only)
#isEvent == 0/1 (search event raid seeds only)
#r.Ability == '1'/'2'/'H'
#r.Nature == 'NATURE'
#r.ShinyType = 'None'/'Star'/'Square'
#r.IVs == spread_name (spread_name = [x,x,x,x,x,x])

from G8RNG import XOROSHIRO,Raid
import socket
import time
import binascii
import signal
import sys

def sendCommand(s, content):
    content += '\r\n' #important for the parser on the switch side
    s.sendall(content.encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.6", 6000))

def signal_handler(signal, frame):
    print("Stop request")
    c = input('Close the game? (y/n): ')
    if c == 'y':
        h = input('Need HOME button pressing? (y/n): ')
        if h == 'y':
            sendCommand(s, "click HOME")
        time.sleep(0.5)
        sendCommand(s, "click X")
        time.sleep(0.8)
        sendCommand(s, "click A")
        time.sleep(1)
    print("Exiting...")
    sendCommand(s, "detachController")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#write den's id in hex (Example: 0xC for Den 12
denOffset_addr = str(0x4298FA70 + (0xC * 0x18))
command = "peek " + denOffset_addr + " 12"

ivfilter = 1 #set 0 to disable filter
Maxresults = 100000
#add the spreads you need
V6 = [31,31,31,31,31,31]
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]

reset = 0

time.sleep(1)
while True:
    sendCommand(s, "click A") #A on game
    print("A on game")
    time.sleep(0.2)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A") #A on profile
    print("A on profile")
    time.sleep(0.2)
    sendCommand(s, "click A")
    time.sleep(16.5) 
    sendCommand(s, "click A") #A to skip anim
    print("Skip animation")
    time.sleep(0.5)
    sendCommand(s, "click A")
    time.sleep(0.5)
    sendCommand(s, "click A")
    time.sleep(8)
    sendCommand(s, "click A") #A on den
    print("A on den")
    time.sleep(0.5)
    sendCommand(s, "click A")
    time.sleep(1.3)
    sendCommand(s, "click A") #A to throw whishing piece
    print("Throw Wishing Piece in den")
    time.sleep(1.4)
    sendCommand(s, "click A") #A to save
    print("Saving")
    time.sleep(0.8)
    sendCommand(s, "click HOME") #Home
    print("HOME clicked")
    time.sleep(0.5)

    sendCommand(s, command) #get denOffset
    time.sleep(0.5)
    denOffset = s.recv(25)

    seed = int.from_bytes(binascii.unhexlify(denOffset[0:16]), "little") #den Seed
    print("Seed:", hex(seed))

    flag_rb = int.from_bytes(binascii.unhexlify(denOffset[20:-3]), "big") #rare beam byte
    #print(hex(flag_rb))
    flag_rb = (flag_rb > 0) and (flag_rb & 1) == 0 #rare beam check

    if flag_rb:
        isRare = 1
        print("Rare beam")
    else:
        isRare = 0
        print("No rare beam")

    flag_e = int.from_bytes(binascii.unhexlify(denOffset[22:-1]), "big") #event den byte
    #print(hex(flag_e))
    flag_e = (flag_e >> 1) & 1 #event raid check

    if flag_e:
        isEvent = 1
        print("Event raid")
    else:
        isEvent = 0
        print("No event raid")

    #spreads search
    j = 0
    found = 0
    while j < Maxresults: #and isEvent == 1/isRare == 1:
        if j < 1:
            print("Searching...")

        r = Raid(seed, flawlessiv = 5, HA = 1, RandomGender = 1)
        seed = XOROSHIRO(seed).next()
        if ivfilter:
            if r.ShinyType != 'None' and r.Nature == 'RELAXED' and r.Ability == 'H': #and (r.IVs == V6 or r.IVs == A0 or r.IVs == S0):
                print("Frame: ", j)
                r.print()
                found = 1
        else:
            found = 1
            print("Frame: ", j)
            r.print()
        j += 1

    if found:
        print("Found after", reset, "resets")
        a = input('Continue searching? (y/n): ')
        if a != "y":
            c = input('Close the game? (y/n): ')
            if c == 'y':
                time.sleep(0.5)
                sendCommand(s, "click X")
                time.sleep(0.8)
                sendCommand(s, "click A")
                time.sleep(3.5)
            sendCommand(s, "detachController")
            break
    else:
        if j == 0:
            print("Research skipped")
            
        reset = reset + 1
        print("Nothing found - Resets:", reset)

    time.sleep(0.5)
    sendCommand(s, "click X")
    time.sleep(0.8)
    sendCommand(s, "click A")
    time.sleep(3.5)
    print()
