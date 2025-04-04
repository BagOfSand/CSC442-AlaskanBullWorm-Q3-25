from ftplib import FTP
METHOD = 10

#ip =" localhost"
IP = "138.47.99.228"
PORT = 21
USER = "anonymous"
PASSWORD = ""

if(METHOD == 7):
    FOLDER = "/7/"
else:
    FOLDER = "/10/"

#if you code timesout, this miht the constant to change
USE_PASSIVE = True

#Connect and log into
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)

ftp.set_pasv(False)

#navigate to the appropriate folder
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

#exit the ftp server
ftp.quit()

#try and display each file
for f in files:
    print(f)

if(METHOD == 7):
    perms = [perm[:10] for perm in files if perm.startswith('---')]
else:
    perms = [perm[:10] for perm in files]
binarystring = ""
if METHOD == 10:
    permissions = "".join(perms)
    for perm in permissions:
        for i in range(len(perm)):
            if perm[i] == "-":
                binarystring += "0"
            else:
                binarystring += "1"    
else:
    for i in range(len(perms)):
        for j in range(3,len(perms[i])):    
            if(perms[i][j]) == "-":
                binarystring += "0"
            else:
                binarystring += "1"

chunks = [binarystring[i:i+7] for i in range(0, len(binarystring), 7)]
decoded_message = ""
for i in range(0, len(binarystring), 7):
    chunk = binarystring[i:i + 7]

    if len(chunk) < 7:
        continue  # Skip incomplete chunks

    decimal_value = int(chunk, 2)

    # Ensure the decimal value is within printable ASCII range
    if 32 <= decimal_value <= 126:  # Printable ASCII characters
        decoded_message += chr(decimal_value)

print(decoded_message)