#!/bin/bash

# brute force retrieve file from a steg-file wrapper

read -p "Enter the name of the wrapper.file: " wrapper
read -p "Enter the mode (b for bit, B for byte): " mode
read -p "Enter the maximum offset (inclusive): " max_offset
read -p "Enter the maximum increment to test (inclusive): " max_increment

echo ""

echo "Making temp folder to hold brute attempts"

mkdir "$wrapper-brute"
cp Steg.py ./"$wrapper-brute" # copy Steg over for the program to use
cp $wrapper ./"$wrapper-brute" # copy wrapper over
cd "$wrapper-brute"

offset=2
increment=2
int=1


echo "Entering brute force for steg.py:"
echo "* To edit looping features, open the .sh file with VIM"
echo "Passing through to loop:"

until [[ offset -gt $max_offset ]]
do
	let increment=2
	until [[ increment -gt $max_increment ]]
	do
		echo "-- Pass $int: -o$offset and -i$increment"
		python3 Steg.py -r -$mode -o$offset -i$increment -w$wrapper > _pass$int
		
		# Increase the increment to test
		# IF THE INCREMENT IS WEIRD, THEN THIS IS THE PART TO CHANGE
		let increment=increment*2

		# You don't want to change this: this renames the files so they don't overwrite each other.
		let int=int+1
	done

	# increase the offset to test
	# IF THE OFFSET IS WEIRD, THEN THIS IS THE PART TO CHANGE
	
	#let offset=offset-1
	# BY DEFAULT, TEST EACH OFFSET AT A MULTIPLE OF 2
	let offset=offset*2
	
	#let offset=offset+1
done

echo "Brute force steg complete. Open the new folder to view derived files."
cd ..



