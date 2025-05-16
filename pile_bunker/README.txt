Useful information:
- Miscellaneous classnotes are first in this file
- Under this short section is the long Python executables section that explains how they are used (roughly)
- https://enigmatics.org/tools/brute - a wonderful website for brute-forcing certain ciphers
- the folder called "labs" has the lab procedure PDFs included, along with some other stuff
- I made this shit at midnight the night before Cyberstorm so please don't be too mad at me if some of the
    program use cases are poorly defined, bro I'm just as confused as you are




LONG LIVE THE BULLWORM.





=======================================================================================================
MISCELLANEOUS NOTES:
=======================================================================================================


NMAP – how to knock on everyone’s door and make people very very mad at you

nmap -pn IP.ADDRESS.GOES.HERE
- your one-stop shop to learning about an IP address through Port knocking – systematically 
    slamming your packets against the closed doors of the computer’s ports until it lets you in

nmap 123.45.67.1/24
- a lot weirder, and takes a very long time.

(For kali vm challenges on the website, sudo password is “kali”)


“sudo nmap -sV ipaddress”


SSH look up metasploit – default login and password are msfadmin


If you’re nmapping, your process might look like this:
    • If you have an IP address, then nmap it. If you only have the first three, then you can do 
        “nmap XXX.XXX.XXX.1/24” to get data on what’s at the address
    • Look through the list. Find anything you recognize. Keywords should be like “SSH”, “FTP”, or “Metasploit”
    • If the IP address has a server on it, you can try logging in with the default credentials 
        for the system. Look it up on google. 
        ◦ For example, the default login and password for metasploit is “msfadmin”. Worst-case 
            scenario, you can brute force a login with Hydra.

Hydra is funny
    • You can brute-force passwords. It takes a while
    • You can make or find a long list of commonly used passwords to test.
    • Alternatively you can use online tools.
    • Go to find the way to brute force the parts you want
    • type “hydra -l username -P path/to/wordlist.txt host_ip ssh” for ssh servers
    • for ftp, it’s similar: “hydra -l username -P path/to/wordlist.txt ftp://host_ip”


“msfconsole” on a system with metasploit
    • zany enter info
    • Press “?” for info
        ◦ “search” – under module names and descriptions – search for information on the IP address
            ▪ “search http" will give you the exploits for an http server (may need to make more specific query)
            ▪ “search vsftpd” will give you the exploits for this thing
            ▪ “use [num]” where num is the number of the exploit that has the best rating
            ▪  “show options” will show you the module options for the “use” that you entered
                • Enter the required information
                • Target host would be the machine you want access to
            ▪ type “run” to run the machine
            ▪ if it worked, you now have access to the machine. Use normal shell commands.
            ▪ Type “exit” to exit the console.
    • Use auxiliary/scanner/ftp/ftp_login



=======================================================================================================
HOW TO USE THE PYTHON FILES:
=======================================================================================================


======================== textToBinary.py ========================
Written by Sean

python3 textToBinary.py

Description:
    After running the file, into the terminal insert the text that should be passed through the binary converter.
    Press enter, and the returned output should give you successflly sanitized binary.
    
    You can VIM open the python file to change what is recognized as binary. By default, the word "one" and "zero" stand
    for 1 and 0. Changing the string changes what is recognized.

    It's best to copy and paste the text to translate into the terminal, but you can use redirects
    to pipe a file's contents into the program.

Example usage:
python3 textToBinary.py
onezeroone one onnne zero zzeeerone #(I typed this, then entered)
101101

python3 textToBinary.py < test.txt #(test.txt contains strings with "one" and "zero" in it)
10

Hints and Giveaways:
- janky 'binary' with "one" and "zero", or maybe "i" and "o". 






======================== binary.py ========================

python3 binary.py < contentsToTranslate.txt

Description:
    Redirect the contents of a binary file into the program. The contents are converted to ASCII and 
    printed to terminal.

Example usage:
python3 binary.py < test4.txt

Hints and Giveaways:
- ...it's binary







======================== vigenere.py ========================
Written by Sean

python3 vigenere.py -(ed) key
- e = encode, d = decode
- key = string key to apply character shift

Description:
    After running the file, into the terminal insert the text that should be passed through the cipher. Press enter,
    and the returned output should give you the pass.

    Notice: If you want to apply the same key to text repeatedly, you can press "enter" to apply the key 
    to the newly generated string.


Example usage:
python3 vigenere.py -e mykey
hello #(I typed this)
tcvpm
    #(pressed enter to apply key again)
faftk
    #(pressed enter)
rypxi
^C  #(control c to exit)

Example usage 2:
#(assume ciphertext.text had text in it)
python3 vigenere.py -d "This is my key" < ciphertext.text
This is text that was translated with the key. #(ciphertext.text's contents were piped into the program and decoded with key)


Hints and Giveaways:
- gibberish is usually a giveaway. If you're unsure, use the BRUTE website at the top of this file.






======================== fetch.py ========================


python3 fetch.py

Description: 
    Fetch the contents of an FTP server, within a specified directory, and translate the file permissions of the files/folders
    in said directory into binary.

    Has a 10-bit and 7-bit version. (under variable METHOD at the top)

    Need to specify:
    - IP Address
    - Port (for FTP, should be 21)
    - Username
    - Password
    - The destination folder 


No notable example

Hints and Giveaways:
- an FTP server with a bunch of gibberish files in it, each with unique read/write privileges.
    - more likely to be a fetch.py problem if there's a *lot* of files to go through.






======================== timelock.py ========================

python timelock.py

Description:
    Generates a unique 4-character string append. Meant to be added on to the end of a password that updates once every 60seconds.
    
    Before running, please make sure to install pytz library.

    You may need to manually change the epoch specified by the program. Running the program will ask for an Epoch.
    If you have no Epoch, default to using the standard ()

    Example epoch input: 2025 05 09 11 43 00

    You can manually set the current time by setting MANUAL to True and changing the current_time_str string.


Hints and Giveaways:
- some_stringXXXX, or some_stringXXXXY.







======================== chat_client.py ========================
Written by Keahi

python chat_client.py

Description:
    Taps into a chat server, and grabs an overt message. Charts the time delay between each character being sent, and maps the
    delay to either 1 or 0. Compiles a message from the bits to make the covert message.
    
    Supposed to end when an EOF is encountered.
    Need to specify:
    - PORT
    - SERVER_IP
    - THRESHOLD_0
    - THRESHOLD_1

    NOTE 2:Apparently, running this code on Windows gives different timings. The profs. don't recommend running it on Windows.

Hints and Giveaways:
- given an IP address and port, but no way to log in. May want to check if an overt message is being broadcast from that port.






======================== timing.py ========================
Writte by Jianna

Same usecase as chat_client, but with a few differences: 
    Need to specify:
    - IP Address
    - Port
    - delayPoint

    NOTE 1: You may need to switch around which delay is 0 and which is 1. To do that, keep track of where the
    "delayPoint" variable is used. You may need to change a "<" to a ">" or vice versa.






======================== xor.py ========================
Written by Luka and Reagan

python3 xor.py file1 file2 > output

Description:
    Two files of the same size can have each bit Exclusive-Or'd against each other to make an unrecognizable file.


Hints and Giveaways:
- Exactly two unreadable files of the exact same size are a dead giveaway.






======================== Steg.py ========================
Steg.py written by Luka
steg.sh BASH file written by Sean

python Steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]
- brackets are optional / only needed sometimes
- you can skip formatting if you run "bash steg.sh"

Description:
    Literally just run the bash file with "bash steg.sh" and follow the written steps. It's that dead simple.

    You may need to edit the bash file if the interval we need to test is particularly odd.
    In that case, VIM open the bash script and edit at the marked portion, OR just ask Sean to do it.

Hints and Giveaways:
- an image with visual artifacts at regular intervals is easy to spot
- other files can have this too - look for strange artifacts in text or formatting at regular intervals.
- In BMP images or other image types, you may have a hard time finding bit-encoded data. Use brute force when necessary.

"When a gun don't work, use more gun"
    - Engineer TF2 (or something like that)





