#Connect your Switch to Interet
#Start sys-botbase and ldn_mitm
#Go to System Settings, check your Switch IP and write it below
#Set game text speed to normal
#Save in front of an empty Den(get its watts before saving if they're avaiable). You must have at least one Wishing Piece in your bag
#Start the bot with game closed and selection square over it
#r.Ability == '1'/'2'/'H'
#r.Nature == 'NATURE'
#r.ShinyType == 'None'/'Star'/'Square' (!= 'None' for both square/star)
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

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    c = input('Close the game? (y/n): ')
    if c == 'y':
        h = input('Need HOME button pressing? (y/n): ')
        if h == 'y':
            sendCommand(s, "click HOME")
        time.sleep(0.5)
        sendCommand(s, "click X")
        time.sleep(0.2)
        sendCommand(s, "click X")
        time.sleep(0.8)
        sendCommand(s, "click A")
        time.sleep(0.2)
        sendCommand(s, "click A")
        time.sleep(1)
    print("Exiting...")
    sendCommand(s, "detachController")
    sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.3", 6000)) #write the IP of your Switch here

signal.signal(signal.SIGINT, signal_handler)

ivfilter = 1 #set 0 to disable filter

V6 = [31,31,31,31,31,31] #add here the spreads you need
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]

reset = 0
rb_research = 0
ev_research = 0
isToxtricity = 0

denId = int(input("Den Id: "))
if denId > 16:
    denId += 1
denOffset_addr = str(0x4298FA70 + (denId * 0x18))
command = "peek " + denOffset_addr + " 12"

rb_research = input("Are you looking for a Rare Beam Raid? (y/n) ")
if rb_research == "y":
    rb_research = 1
else:
    rb_research = 0
    ev_research = input("Are you looking for an Event Raid? (y/n) ")
    if ev_research == "y":
        ev_research = 1
    else:
        ev_research = 0

isToxtricity = input("Are you looking for Toxtricity? (y/n) ")

if isToxtricity == 'y':
    game_version = input("Game? (Sw/Sh) ")
    if game_version == 'Sw':
        isToxtricity = 1
    else:
        isToxtricity = 2

Maxresults = int(input("Input Max Results: "))

time.sleep(0.5)
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
    print("Seed:", str(hex(seed))[2:18].upper())

    flag_rb = int.from_bytes(binascii.unhexlify(denOffset[20:-3]), "big") #rare beam byte
    #print(hex(flag_rb))
    flag_rb = (flag_rb > 0) and (flag_rb & 1) == 0 #rare beam check

    if flag_rb:
        print("Rare beam")
    else:
        print("No rare beam")

    flag_ev = int.from_bytes(binascii.unhexlify(denOffset[22:-1]), "big") #event den byte
    #print(hex(flag_e))
    flag_ev = (flag_ev >> 1) & 1 #event raid check

    if flag_ev:
        print("Event Raid")
    else:
        print("No event Raid")

    #spreads research
    j = 0
    found = 0
    do_research = 1
    
    if rb_research == 1 and rb_research != flag_rb: #rare beam/event check
        do_research = 0
    elif ev_research == 1 and ev_research != flag_ev:
        do_research = 0
    elif rb_research == 0 and ev_research == 0:
        if rb_research != flag_rb or ev_research != flag_ev:
            do_research = 0
    
    while j < Maxresults and do_research:        
        if j < 1:
            print("Searching...")

        r = Raid(seed,isToxtricity, flawlessiv = 5, HA = 1, RandomGender = 1)
        seed = XOROSHIRO(seed).next()
        if ivfilter:
            if r.ShinyType != 'None' and r.Nature == 'ADAMANT' and r.Ability == 'H': #and (r.IVs == V6 or r.IVs == A0 or r.IVs == S0):
                print("Frame: ", j)
                r.print()
                if found != 1:
                    found = 1
        else:
            if found != 1:
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
                print("Closing game...")
                sendCommand(s, "click X")
                time.sleep(0.8)
                sendCommand(s, "click A")
                time.sleep(3.5)
            print("Exiting...")
            sendCommand(s, "detachController")
            break
    else:
        if j == 0:
            print("Research skipped")
            
        reset = reset + 1
        print("Nothing found - Resets:", reset)

    #game closing
    time.sleep(0.5)
    sendCommand(s, "click X")
    time.sleep(0.2)
    sendCommand(s, "click X")
    time.sleep(0.8)
    sendCommand(s, "click A")
    time.sleep(0.2)
    sendCommand(s, "click A")
    time.sleep(3.5)
    print()
