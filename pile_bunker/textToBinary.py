import sys

for line in sys.stdin:
    # whatever the input is should be read
    inputString = line.rstrip()

    # change these to whatever BS the prof. says it's supposed to be. Like "i" for 1 and "o" for 0.
    zero = "zero"
    one = "one"

    # replaces the "fake" ones and zeros with actual binary.
    inputString = inputString.replace(one, "1")
    inputString = inputString.replace(zero, "0")

    # compile the result by trimming any excess
    result = ""
    for char in inputString:
        if char == "1" or char == "0":
            result+=char


    # return output
    print(result)
