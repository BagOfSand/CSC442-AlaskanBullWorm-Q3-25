#Before running please make sure to install pytz library

from datetime import datetime
import pytz
import hashlib
import time
#Set timezone
timezone = pytz.timezone('US/Central')  

DEBUG = True
MANUAL = False

#Get Epoch Time
epoch_input = input()

# seconds since the international standard epoch: time.time()
# example of an Epoch: 2017 01 01 00 00 00

while True:

    #For Debug purposes
    if(MANUAL == True):   
        current_time_str = "2025 05 09 11 43 00"
        current_time = datetime.strptime(current_time_str, "%Y %m %d %H %M %S")
        current_time = timezone.localize(current_time)
    else: 
        current_time = datetime.now(pytz.timezone('US/Central'))



    #Parse into datetime object
    epoch_time = datetime.strptime(epoch_input, "%Y %m %d %H %M %S")
    #Check if DST and fix if so
    epoch_time = timezone.localize(epoch_time)

    #Print times
    print(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Epoch Time: {epoch_time.strftime('%Y-%m-%d %H:%M:%S')}")

    #Subtract current from epoch
    seconds = int((current_time - epoch_time).total_seconds())

    #Before rounding to 60 second interval
    print(f"Raw Seconds difference: {seconds}")

    #Round it
    seconds = seconds - (seconds % 60)

    print(f"Rounded Seconds: {seconds}")

    seconds = str(seconds)


    #Hash it out
    def convert_time_to_pass(input):
        key = ""
        
        # Create the MD5 hash object
        hash_slinging_slasher = hashlib.md5()

        # First round of MD5 hashing with the input
        hash_slinging_slasher.update(input.encode())  # Hash the input
        full_hash = hash_slinging_slasher.hexdigest()  # Get the resulting hash

        if DEBUG:
            print(f"First hash: {full_hash}")
        
        # Second round of MD5 hashing with the first hash
        hash_slinging_slasher = hashlib.md5()  # Reinitialize the hash object for the second round
        hash_slinging_slasher.update(full_hash.encode())  # Hash the first hash
        second_hash = hash_slinging_slasher.hexdigest()  # Get the resulting second hash

        if DEBUG:
            print(f"Second hash: {second_hash}")

        # Extract 2 letters from left to right (a-f)
        count = 2
        for index in range(len(second_hash)):
            if count <= 0:
                break
            elif second_hash[index].isalpha():  # Check if it's a letter
                key += second_hash[index]
                count -= 1

        # Extract 2 digits from right to left (0-9)
        count = 2
        for index in range(len(second_hash) - 1, -1, -1):
            if count <= 0:
                break
            elif second_hash[index].isdigit():  # Check if it's a digit
                key += second_hash[index]
                count -= 1
        
        return key
        
    print(convert_time_to_pass(seconds) )
    time.sleep(2)
