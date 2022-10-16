#!/bin/zsh

# Usage: rename.sh foldername file_to_copy

inputname=$1
mkdir $1

endings=("C" "C#" "D" "D#" "E" "F" "F#" "G" "G#" "A" "A#" "B")

for i in "${endings[@]}"; do
	cp $2 ./$1/$1_$i.wav
done
