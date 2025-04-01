import sys
arguments = sys.argv

direction = arguments[1] # the second argument is the direction of application: 
                            # -e for encode, -d for decode
key = arguments[2].lower()  # the third argument is the key for the cipher
key = key.replace(" ","")

# the capital letters go from ASCII A=65, Z=90
capitals = [65,90]
# lowercase letters go from ASCII a=97, z=122
lowercase = [97,122]

# encodes a character into a hidden ascii value when given a corresponding key character.
# Given two characters as parameters, returns one character.
def encodeChar(inpChar, keyChar):
    # convert the input character and key character into ints
    inpInt = ord(inpChar)
    keyInt = ord(keyChar)
    if keyInt not in range(lowercase[0], lowercase[1]):
        keyInt+=lowercase[0]

    # if the input character is a capital letter (between ascii values 65 and 90, inclusive)
    if inpInt in range(capitals[0], capitals[1]+1):
        # then the displacement is relative to the uppercase bound
        displace = (inpInt-capitals[0]) + (keyInt-lowercase[0])
        displace %= 26
        # convert to character and return
        return chr(65+displace)
    # if the input character is a lowercase letter (between ascii values 97 and 122, inclusive)
    elif inpInt in range(lowercase[0], lowercase[1]+1):
        # then the displacement is relative to the lowercase bound
        displace = (inpInt-lowercase[0]) + (keyInt-lowercase[0])
        displace %= 26
        # convert to character and return
        return chr(97+displace)
    # if the input character is neither an uppercase or lowercase letter, pass it through
    return inpChar


# decodes a character into the hidden ascii value when given a corresponding key character.
# Given two characters as parameters, returns one character.
def decodeChar(inpChar, keyChar):
    # convert the input character and key character into ints
    inpInt = ord(inpChar)
    keyInt = ord(keyChar)

    # if the input character is a capital letter (between ascii values 65 and 90, inclusive)
    if inpInt in range(capitals[0], capitals[1]+1):
        # then the displacement is relative to the uppercase bound
        displace = (inpInt-capitals[0]) - (keyInt-lowercase[0])
        displace %= 26
        # convert to character and return
        return chr(65+displace)
    # if the input character is a lowercase letter (between ascii values 97 and 122, inclusive)
    elif inpInt in range(lowercase[0], lowercase[1]+1):
        # then the displacement is relative to the lowercase bound
        displace = (inpInt-lowercase[0]) - (keyInt-lowercase[0])
        displace %= 26
        # convert to character and return
        return chr(97+displace)
    # if the input character is neither an uppercase or lowercase letter, pass it through
    return inpChar



# Enter main loop
while(True):
    beforeProcessing = input()
    resultString = ""
    # split the string into a list of characters
    # for each character in the string, encode or decode depending on what the parameters were
    encodingIndex = 0
    keyIndex = 0
    while ( encodingIndex < len(beforeProcessing)):
        if(direction == "-e"):
            resultString += (encodeChar(beforeProcessing[encodingIndex], key[keyIndex]))
        elif(direction == "-d"): 
            resultString += (decodeChar(beforeProcessing[encodingIndex], key[keyIndex]))
        else:
            sys.exit("Invalid parameter. Select '-e' for encoding, or '-d' for decoding")
        
        if(beforeProcessing[encodingIndex] != " "): # if we encoded a space, the key index is not incremented
            keyIndex = (keyIndex+1)%len(key)
        encodingIndex+=1

    print(resultString)


"""
thanks geeksForGeeks for info on how to convert a string list into ascii values

working to find out how non-letter characters in keys work
'r' + ' ' = 'j'
114 + 32 = 106
a = 97, r is letter #18, so index 17
9 away from 'a' is 'j'

'r' + 's' = 'j'
114 + 115 = 106
#18 + #19 = #10
a = 97, r is letter #18, so index 17
9 away from 'a' is 'j'

"""
