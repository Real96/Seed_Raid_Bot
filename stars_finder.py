#Connect your Switch to Interet
#Start sys-botbase, ldn_mitm and luxray (the yellow cursor of luxray has to be over "+3" button)
#Go to System Settings, check your Switch IP and write it below
#Save in front of an Den whose beam has been generated through Wishing Piece
#Start the bot with game closed and selection square over it

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
            time.sleep(0.5)
            sendCommand(s, "click HOME")
        time.sleep(0.5)
        print("Closing game...")
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
s.connect(("192.168.1.2", 6000)) #write the IP of your Switch here

signal.signal(signal.SIGINT, signal_handler)

reset = 0

denId = int(input("Den Id: "))
if denId > 16:
    denId += 1
denOffset_addr = str(0x4298FA70 + (denId * 0x18))
command = "peek " + denOffset_addr + " 12"

stars = int(input("Which number of Stars are you looking for? (1 to 5) "))

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
    time.sleep(9)
    sendCommand(s, "click R") #R on Luxray "+3" button
    time.sleep(1.5)
    
    sendCommand(s, command) #get denOffset
    time.sleep(0.5)
    denOffset = s.recv(25)
    
    stars_byte = int.from_bytes(binascii.unhexlify(denOffset[16:-7]), "big") #raid stars
    print("Raid stars:", stars_byte + 1)
    time.sleep(0.5)

    if stars_byte + 1 == stars:
        print("Found after", reset, "resets")
        a = input('Continue searching? (y/n): ')
        if a != "y":
            c = input('Close the game? (y/n): ')
            if c == 'y':
                time.sleep(0.5)
                sendCommand(s, "click HOME")
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
        reset = reset + 1
        print("Wrong Stars - Resets:", reset)

    #game closing
    time.sleep(0.5)
    sendCommand(s, "click HOME")
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
