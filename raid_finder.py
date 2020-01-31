#Set game text speed to slow
#Save in front of a Den. You must have at least one Wishing Piece in your bag
#Start the bot with game closed and selection square over it
#Den Seed address: "peek 0xaddress 8" (address = 0x4298FA70 + (0xden_id) * 0x18)) Example: 0x4298FB78 Den 11
#Rare beam flag byte address = "peek 0xaddress 1" (address = 0x4298FA7A + (0xden_id) * 0x18) Example: 0x4298FB82 Den 11
#Event flag byte address = "peek 0xaddress 1" (address = (0x4298FA7B + (0xden_id) * 0x18)) Example: 0x4298FB83 Den 11
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

def sendCommand(s, content):
    content += '\r\n' #important for the parser on the switch side
    s.sendall(content.encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.7", 6000))

reset = 0
ivfilter = 1 #set 0 to disable filter
Maxresults = 100000
#add the spreads you need
V6 = [31,31,31,31,31,31]
A0 = [31,0,31,31,31,31]
S0 = [31,31,31,31,31,0]

time.sleep(2)
while True:
    sendCommand(s, "click A") #A on game
    print("A in game")
    time.sleep(0.2)
    sendCommand(s, "click A")
    time.sleep(1.5)
    sendCommand(s, "click A") #A on profile
    print("A in profile")
    time.sleep(0.2)
    sendCommand(s, "click A")
    time.sleep(16.5) 
    sendCommand(s, "click A") #A to skip anim
    print("skip anim")
    time.sleep(1)
    sendCommand(s, "click A")
    time.sleep(1)
    sendCommand(s, "click A")
    time.sleep(8)
    sendCommand(s, "click A") #A in den
    print("A in den")
    time.sleep(0.5)
    sendCommand(s, "click A")
    time.sleep(2)
    sendCommand(s, "click A") #A to throw whishing piece
    print("throw piece in den")
    time.sleep(1.8)
    sendCommand(s, "click A") #A to save
    print("saving")
    time.sleep(1)
    sendCommand(s, "click HOME") #Home
    print("HOME clicked")
    time.sleep(1.5)

    sendCommand(s, "peek 0x4298FB82 1") #rare beam byte
    time.sleep(0.5)
    rarebeambyte = s.recv(3)
    #print(binascii.unhexlify(rarebeambyte[0:-1]))
    
    flag_rb = int.from_bytes(binascii.unhexlify(rarebeambyte[0:-1]), "big") #rare beam flag
    flag_rb = (flag_rb > 0) and (flag_rb & 1) == 0

    if flag_rb:
        isRare = 1
        print("Rare beam")
    else:
        isRare = 0
        print("No rare beam")
    
    sendCommand(s, "peek 0x4298FB83 1") #event den byte
    time.sleep(0.5)
    eventbyte = s.recv(3)
    #print(binascii.unhexlify(eventbyte[0:-1]))
    
    flag_e = int.from_bytes(binascii.unhexlify(eventbyte[0:-1]), "big") #event den flag
    flag_e = (flag_e >> 1) & 1

    if flag_e:
        isEvent = 1
        print("Event raid")
    else:
        isEvent = 0
        print("No event raid")
    
    sendCommand(s, "peek 0x4298FB78 8") #get reversed seed from ram
    time.sleep(0.5)
    re_seed = s.recv(17)
    re_seed = (binascii.unhexlify(re_seed[0:-1])).hex()
    #print(re_seed)
    seed = int.from_bytes(binascii.unhexlify(re_seed), "little") #reverse the seed
    print("Seed:", hex(seed))
    print("Searching...")

    #spread searh
    j = 0
    found = 0
    while j < Maxresults: #and isEvent == 1/isRare == 1:
        r = Raid(seed, flawlessiv = 5, HA = 1, RandomGender = 1)
        seed = XOROSHIRO(seed).next()
        if ivfilter:
            if r.ShinyType != 'None' and r.Nature == 'RELAXED' and r.Ability == 'H': #and (r.IVs == V6 or r.IVs == A0 or r.IVs == S0):
                print(j)
                r.print()
                found = 1
        else:
            r.print()
        j += 1

    if found:
        print("Found after", reset, "resets")
        a = input('Continue? (y/n): ')
        if a != "y":
            c = input('Close the game? (y/n): ')
            if c == 'y':
                time.sleep(0.5)
                sendCommand(s, "click X")
                time.sleep(0.5)
                sendCommand(s, "click A")
                time.sleep(3.5)
            break
    else:
        reset = reset + 1
        print("Nothing found - resets:", reset)

    time.sleep(0.5)
    sendCommand(s, "click X")
    time.sleep(0.5)
    sendCommand(s, "click A")
    time.sleep(3.5)
    print()
