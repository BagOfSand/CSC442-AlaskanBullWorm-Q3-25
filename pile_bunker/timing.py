from time import time
import socket
from sys import stdout

# enables debugging output
DEBUG = False
delayPoint = 0.04

# server variables
ip = '138.47.99.228'
port = 31337

# connect to the chat server
stdout.write("[connect to the chat server]\n")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# receive an overt message
data = s.recv(4096).decode()
delays = []
while (data.rstrip("\n") != "EOF"):

    # display overt message as it's being received (to stdout)
    stdout.write(data) # output the data
    stdout.flush()

    # get delays
    while(len(data) > 1):
        delays.append(0)
        data = data[1:]

    # time the delays between characters received of an overt message
    t0 = time()
    data = s.recv(4096).decode()
    t1 = time()

    # calculate the time delta and add to list of delays
    delta = round(t1 - t0, 3)
    delays.append(delta)

    # output if debugging
    if (DEBUG):
        stdout.write(" {}\n".format(delta))
        stdout.flush()

stdout.write("[disconnect from the chat server]\n") # disconnect from server
stdout.write("\nDELAYS: ")
stdout.write("".join(str(delays))) # delays between characters
s.close()

# determine map of delays
binaryMessage = ""
for i in delays:
    if i > delayPoint:
        binaryMessage += "1"
    else:
        binaryMessage += "0"

stdout.write("\n\nBINARY MESSAGE: ") # disconnect from server
stdout.write(str("".join(str((binaryMessage))))) # delays between characters

# convert to ASCII
covertMessage = ""
# figure out if its 7 or 8 bit
if True:
    for idx in range(8, len(binaryMessage), 8):
        # convert the last 8 characters to a binary string
        bin_rep = ''
        for x in range(idx-8, idx, 1):
            bin_rep += str(binaryMessage[x])
        covertMessage += chr(int(bin_rep, 2)) # convert the binary string -> text


# Check for EOF
if covertMessage.endswith("EOF"):
    covertMessage.removesuffix("EOF")

# output the covert message
stdout.write("\n\nCOVERT MESSAGE:") # disconnect from server
stdout.write(covertMessage) # disconnect from server
