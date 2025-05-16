import sys

# get input
contents = sys.stdin.read()

output = ''

# figure out if it's 7 or 8 bit
if (len(contents)-1) % 8 == 0:
    for idx in range(8, len(contents), 8):
        # convert the last 8 characters to a binary string
        bin_rep = ''
        for x in range(idx-8, idx, 1):
            bin_rep += str(contents[x])
        
        output += chr(int(bin_rep, 2)) # convert the binary string -> text
else:
    for idx in range(7, len(contents), 7):
        # convert last 7 characters to a binary string
        bin_rep = ''
        for x in range(idx-7, idx, 1):
            bin_rep += str(contents[x])

        output += chr(int(bin_rep, 2)) # convert the binary string -> text

print(output)
