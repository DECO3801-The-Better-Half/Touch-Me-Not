#!/bin/zsh

# Usage: rename.sh name orinal_note original_offset


# Make the endings array
endings=("C" "C#" "D" "D#" "E" "F" "F#" "G" "G#" "A" "A#" "B")

# get the offset from the note
offset=-100
for i in {1..12}; do
	if [[ "${endings[$i]}" == "$2" ]]; then
		offset=$(((i-1)*100))
	fi
done
# check if the note was found
if [ $offset -eq -100 ]; then
	echo "Invalid note"
	exit 1
fi

# make directory
mkdir $1

# Change pitch and make the new file
# for i in "${endings[@]}"; do
for i in {1..12}; do
	# sox $2 $1/$2_$i.wav pitch $i-$3
	sox $1_$2.wav $1/$1_${endings[$i]}.wav pitch $((((i-1)*100 - $offset + 600) % 1200 - 600))
	# cp $1_$2.wav ./$1/$1_$i.wav
done

# sox sonar_E.wav sonar_D#.wav pitch -100
