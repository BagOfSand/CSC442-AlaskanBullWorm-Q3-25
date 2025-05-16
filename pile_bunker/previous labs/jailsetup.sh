#!/bin/bash
CHROOT='/var/jail'
mkdir -p "$CHROOT"

# loop over the args provided on execution of this file 
# these args are the files we want available in the jail
for file in "$@";
do 
    if [ -x "$file" ] && file "$file" | grep -q 'ELF'
    then
	# For executable files:
        ldd "$file" |      # get the shared libraries for the file
	awk '{print $3}' |     # extract 3rd column (the library filepath)
        grep -E '^/' |     # keep absolute paths (lines starting with /)
        sort -u |          # remove duplicates 
        while read lib;
        do 
           # copy the library and preserve its directory structure
           cp --parents "$lib" "$CHROOT"
        done 
        # copy the file and preserve its directory structure
        cp --parents "$file" "$CHROOT"
    else
	# for non-executable files
	# just copy the file and preserve its directory structure
        cp --parents "$file" "$CHROOT"
    fi 
done 

# Copy the dynamic linker for the architecture of your machine.

# for aarch64 (arm)
if [ -f /lib/ld-linux-aarch64.so.1 ]; then
    cp --parents /lib/ld-linux-aarch64.so.1 "$CHROOT"
fi 

# for amd64 (x86-64)
if [ -f /lib64/ld-linux-x86-64.so.2 ]; then
    cp --parents /lib64/ld-linux-x86-64.so.2 "$CHROOT"
fi 

# for i386 (x86-32)
if [ -f /lib/ld-linux.so.2 ]; then
    cp --parents /lib/ld-linux.so.2 "$CHROOT"
fi 

echo "Ready. Enter the jail with: chroot $CHROOT"
