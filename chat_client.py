import socket
import time
import sys
from binascii import unhexlify

# Settings
# TESTING PORT AND HOST
# PORT = 1337
# SERVER_IP = "localhost"
PORT = 31337
SERVER_IP = "138.47.99.228"
THRESHOLD_0 = 0.05
THRESHOLD_1 = 0.1
DEBUG = True 

def main():
    # Create a socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))

    overt_message = ""
    covert_binary = ""
    last_time = time.time()
    
    # Flag to handle the first character
    # first_char = True

    while True:
        # Measures the time between characters
        char = s.recv(1).decode()
        current_time = time.time()
        delta = round(current_time - last_time, 3)
        last_time = current_time


        # If overt message is recieved, print it. Debug output shows the timing pattern
        if char:
            sys.stdout.write(char)
            sys.stdout.flush()

            # if first_char:
              #  first_char = False
               # continue

            if DEBUG:
                print(" [{:.3f}s]".format(delta))

            # Covert bit detection based on threshold
            if delta < THRESHOLD_1 and delta >= THRESHOLD_0:
                covert_binary += '0'
            elif delta >= THRESHOLD_1:
                covert_binary += '1'

            overt_message += char

            # Stop on EOF
            if overt_message.endswith("EOF"):
                break
        else:
            break

    s.close()

    # Decode the covert binary message into text
    covert_message = ""
    i = 0
    while i + 8 <= len(covert_binary):
        # Get next byte (8 bits)
        b = covert_binary[i:i + 8]

        # Convert to character and add to message
        try:
            covert_message += chr(int(b, 2))
        except Exception:
            covert_message += "?"

        # Check for EOF
        if covert_message.endswith("EOF"):
            break
        
        # Increment
        i += 8

    # Print covert message with and  without the EOF
    print("\nBinary stream:", covert_binary)
    print("\nCovert message: {}".format(covert_message))  
    print("\nCovert message without EOF: {}".format(covert_message[:-3]))  

if __name__ == "__main__":
    main()