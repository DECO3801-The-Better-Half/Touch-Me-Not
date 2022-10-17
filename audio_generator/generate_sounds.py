# sox -m music.mp3 voice.wav mixed.flac

import sys
import subprocess
import random
import json 
# import time
import os
from constants import *

ignored_warnings = [
	"are identical (not copied).",
	"rm:"
]
reduce_volume_warnings = []
def run_command(command: str, use_shell = False) -> tuple[str, str]:
	# print(command)
	process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell)
	stdout, stderr = process.communicate()
	# decode bytes to string
	stdout = stdout.decode("utf-8")
	stderr = stderr.decode("utf-8")
	if stderr:
		if "decrease volume?" in stderr:
			try:
				first_arg_file = command.split(" ")[1].split("/")[1]
			except IndexError: # terrible but i dont care
				first_arg_file = command.split(" ")[3].split("/")[1]
			if first_arg_file not in reduce_volume_warnings:
				# print(f"WARNING: Clipped file: \"{first_arg_file}\". Consider reducing its volume scale factor.")
				reduce_volume_warnings.append(first_arg_file)
				# temp_name = first_arg_file.replace(".wav", "_temp.wav")
				# reduce_volume_warnings.append(f"{temp_name}")
		else:
			for ignored_warning in ignored_warnings:
				if ignored_warning in stderr:
					break
			else:
				print(f"---ERROR from subprocess---\n{command}\n---------------------------\n\n{stderr}\n\n---End of ERROR from subprocess---\nExiting...")
				exit()
	return stdout, stderr

class PanValue:
	def __init__(self, pan_description: str):
		# pan_description is a string of the form "LxRy" where x and y are floats
		self.pan_description = pan_description
		self.left = float(pan_description.split("R")[0][1:])
		self.right = float(pan_description.split("R")[1])

class Layer:
	def __init__(self, file_address: str, note, volume_sf: float):
		self.file_address = file_address
		self.name = file_address.split("/")[-1].split(".")[0]
		self.temp_file_address = f"{TEMP_DIR}/{self.name}.wav"
		self.temp_file_address_no_extension = f"{TEMP_DIR}/{self.name}"
		self.note = note
		self.note_number = note.value
		self.volume_sf = volume_sf

	def __str__(self):
		return f"Layer(name: {self.name}, note: {self.note}, volume_sf: {self.volume_sf})\n"
	def __repr__(self):
		return self.__str__()
	def __hash__(self):
		return hash((self.name, self.note, self.volume_sf))
	def __eq__(self, other):
		if isinstance(other, Layer):
			return self.name == other.name and self.note == other.note and self.volume_sf == other.volume_sf
		return False
	def __ne__(self, other):
		return not self.__eq__(other)

	def get_address_for_note(self, note: Note):
		# print(note)
		if self.note == Note.none:
			return self.temp_file_address
		# print(f"{self.temp_file_address_no_extension}_{note.name}.wav")
		return f"{self.temp_file_address_no_extension}_{note.name}.wav"

	def copy_to_temp_dir(self):
		run_command(f"cp {self.file_address} {self.temp_file_address}")

	def change_wav_volume(self):
		# create temporary file
		run_command(f"cp {self.temp_file_address} {self.temp_file_address_no_extension}_temp.wav")
		run_command(f"rm {self.temp_file_address}")
		# use temporary file to change volume
		run_command(f"sox -v {self.volume_sf} {self.temp_file_address_no_extension}_temp.wav {self.temp_file_address}")
		# delete temporary file
		run_command(f"rm {self.temp_file_address_no_extension}_temp.wav")

	def change_wav_pan(self, pan_value: PanValue):
		# extract left and right channels
		run_command(f"sox {self.temp_file_address} {self.temp_file_address_no_extension}_left_temp.wav remix 1")
		run_command(f"sox {self.temp_file_address} {self.temp_file_address_no_extension}_right_temp.wav remix 2")
		# change volume of each channel
		run_command(f"sox -v {pan_value.left} {self.temp_file_address_no_extension}_left_temp.wav {self.temp_file_address_no_extension}_left.wav")
		run_command(f"sox -v {pan_value.right} {self.temp_file_address_no_extension}_right_temp.wav {self.temp_file_address_no_extension}_right.wav")
		# remove left and right temp files
		run_command(f"rm {self.temp_file_address_no_extension}_left_temp.wav")
		run_command(f"rm {self.temp_file_address_no_extension}_right_temp.wav")
		# remove temp file
		run_command(f"rm {self.temp_file_address}")
		# rejoin the two channels
		run_command(f"sox -M {self.temp_file_address_no_extension}_left.wav {self.temp_file_address_no_extension}_right.wav {self.temp_file_address}")
		# remove left and right files
		run_command(f"rm {self.temp_file_address_no_extension}_left.wav")
		run_command(f"rm {self.temp_file_address_no_extension}_right.wav")

	def generate_all_notes(self):
		if self.note == Note.none:
			return
		for note_number in range(0, 12):
			new_note = Note[Note(note_number).name] #I'm sure this is not how its supposed to be done
			new_file_address = self.get_address_for_note(new_note)
			pitch_value = ((new_note.value - self.note.value + NUM_PITCH_DOWNS) % 12 - NUM_PITCH_DOWNS) * 100
			run_command(f"sox {self.temp_file_address} {new_file_address} pitch {pitch_value}")

class ChordClass:
	def __init__(self, chord, purpose, key = None):
		self.chord = chord # Chord
		self.seventh_chord = Chord[f"{chord.name}_seventh"]
		self.purpose = purpose # ChordPurpose
		self.key = key # If purpose is pivot, this is the key of the pivot chord, if purpose is normal, this is the key of the chord

	# static function used by
	

class Sound:
	def __init__(self, name: str, instrument_name: str, layers: list):
		self.name = name + "_" + instrument_name
		self.sound_type = name
		self.layers = layers
		self.instrument_name = instrument_name

	def __str__(self):
		return f"Sound(name: {self.name},\nlayers:\n{self.layers})\n"
	def __repr__(self):
		return self.__str__()
	def __hash__(self) -> int:
		return hash((self.name, self.instrument_name))
	def __eq__(self, o: object) -> bool:
		if not isinstance(o, Sound):
			return False
		return self.name == o.name and self.instrument_name == o.instrument_name
	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def num_tonal_layers(self):
		return len([layer for layer in self.layers if layer.note != Note.none])

	def get_sound_filenames(self, instrument: 'Instrument', key):
		sound_filenames = []
		# if chord add key first chord
		if instrument.mode == Mode.chord:
			# add key chord
			# if this.num_tonal_layers() < 4:
			# sound_filenames.append(f"{instrument.name}_{key.name}.wav")
			sound_filenames.append(f"{instrument.name}_{self.sound_type}_{key.name}.wav")
			# else:
			# 	sound_filenames.append(f"{instrument.name}_{key.name}_seventh.wav")
		# if arpeggio or scale add key arpeggio notes
		elif instrument.mode == Mode.arpeggio or instrument.mode == Mode.scale:
			for note_number in SCALE_INDEX_IN_MODE[instrument.mode]:
				note = SCALES[key][note_number]
				# sound_type = this.name.split("_")[0]
				# print(sound_type)
				sound_filenames.append(f"{instrument.name}_{self.sound_type}_{note.name}.wav")

		return sound_filenames


	def merge_layer(self, new_sound_address, new_layer_address):
		temp_new_sound_address = new_sound_address.replace(".wav", "_temp.wav")
		temp_new_layer_address = new_layer_address.replace(".wav", "_temp.wav")
		# copy the files to a temp file to work on and merge
		run_command(f"cp {new_sound_address} {temp_new_sound_address}")
		run_command(f"rm {new_sound_address}")
		run_command(f"cp {new_layer_address} {temp_new_layer_address}")
		# get duration of both files to merge
		stdout, stderr = run_command(f"soxi -D {temp_new_sound_address}")
		new_sound_duration = float(stdout)
		stdout, stderr = run_command(f"soxi -D {temp_new_layer_address}")
		new_layer_duration = float(stdout)
		if new_sound_duration != new_layer_duration and "impact" not in self.name:
			# clip the longer file
			if new_sound_duration > new_layer_duration:
				# trim sound
				run_command(f"cp {temp_new_sound_address} {temp_new_sound_address.replace('.wav', '_temp.wav')}")
				run_command(f"rm {temp_new_sound_address}")
				run_command(f"sox {temp_new_sound_address.replace('.wav', '_temp.wav')} {temp_new_sound_address} trim 0 {new_layer_duration}")
				run_command(f"rm {temp_new_sound_address.replace('.wav', '_temp.wav')}")
			else:
				# trim layer
				run_command(f"cp {temp_new_layer_address} {temp_new_layer_address.replace('.wav', '_temp.wav')}")
				run_command(f"rm {temp_new_layer_address}")
				run_command(f"sox {temp_new_layer_address.replace('.wav', '_temp.wav')} {temp_new_layer_address} trim 0 {new_sound_duration}")
				run_command(f"rm {temp_new_layer_address.replace('.wav', '_temp.wav')}")

		# merge the files
		run_command(f"sox -m {temp_new_layer_address} {temp_new_sound_address} {new_sound_address}")
		# delete the temp files
		run_command(f"rm {temp_new_sound_address}")
		run_command(f"rm {temp_new_layer_address}")

	# 	for chord in self.chords:
	# 		if chord.key == key:
	# 			if seventh_chord:
	# 				return f"{sound.name}_{chord.seventh_chord.name}_{note.name}.wav"
	# 			else:
	# 				return f"{sound.name}_{chord.chord.name}_{note.name}.wav"

	def generate(self, instrument: 'Instrument'):
		# sort layers by highest volume_sf to lowest
		self.layers.sort(key=lambda layer: layer.volume_sf, reverse=True)

		# generate all the layers
		for layer in self.layers:
			layer.copy_to_temp_dir()
			layer.change_wav_volume()
			layer.change_wav_pan(instrument.pan_value)
			layer.generate_all_notes()
		
		# generate all the single tones
		if instrument.mode == Mode.scale or instrument.mode == Mode.arpeggio:
			for note_number in range(0, 12):
				new_note = Note(note_number)
				new_sound_address = f"{TEMP_DIR}/{instrument.name}_{self.name}_{new_note.name}.wav"
				# join all the relevant layers
				for i, layer in enumerate(self.layers):
					if i == 0:
						run_command(f"cp {layer.get_address_for_note(new_note)} {new_sound_address}")
					else:
						self.merge_layer(new_sound_address, layer.get_address_for_note(new_note))
				# print(f"CREATING: {instrument.name} {self.name} note: {new_note.name}")

		# generate all the chords
		for chord in instrument.chords:
			# ignore other normal chords if purpose is normal and mode is scale or arpeggio
			# TODO read this
			# if chord.purpose == ChordPurpose.normal and instrument.mode != Mode.chord:
			# 	continue
			new_sound_address = f"{TEMP_DIR}/{instrument.name}_{self.name}_{chord.chord.name}.wav"
			# count how many layers have a tune
			num_chord_notes = 0
			for layer in self.layers:
				if layer.note != Note.none:
					num_chord_notes += 1
			# get the notes of the chord
			chord_notes = []
			# seventh chord
			if num_chord_notes <= 4:
				chord_notes = CHORD_NOTES[chord.seventh_chord]
			# normal chord
			else:
				chord_notes = CHORD_NOTES[chord.chord]
			# if too many layers extend the chord_notes to wrap around
			if num_chord_notes > len(chord_notes):
				chord_notes = chord_notes * ((num_chord_notes // len(chord_notes)) + 1)
				# remove extra notes
				chord_notes = chord_notes[:num_chord_notes]
			# shuffle the notes
			chord_notes = random.sample(chord_notes, num_chord_notes)
			# print the chord and chord notes
			# print(f"CREATING: {instrument.name} {self.name} chord: {chord.chord.name}, notes: {[note.name for note in chord_notes]}")
			# join all the relevant layers
			merged_layers = []
			for i, layer in enumerate(self.layers):
				# choose chord note
				closest_note = Note.A
				if layer.note != Note.none:
					closest_note = chord_notes[0]
				closest_note_distance = abs((closest_note.value - layer.note.value + NUM_PITCH_DOWNS) % 12 - NUM_PITCH_DOWNS)
				for note in chord_notes:
					# find distance from current note to note in chord
					distance = abs((note.value - layer.note.value + NUM_PITCH_DOWNS) % 12 - NUM_PITCH_DOWNS)
					# if distance is smaller, set closest note to current note
					if distance < closest_note_distance:
						closest_note = note
						closest_note_distance = distance
				# remove note from chord notes if the layer is tonal
				if layer.note != Note.none:
					chord_notes.remove(closest_note)
				# merge in the layer
				# print what is about to happen
				# print(f"MERGING layer {layer.name} with {closest_note.name} of chord {chord.chord.name}")
				if i == 0:
					run_command(f"cp {layer.get_address_for_note(closest_note)} {new_sound_address}")
				else:
					self.merge_layer(new_sound_address, layer.get_address_for_note(closest_note))
				merged_layers.append(layer)
			# print the layers that were merged
			# print(f"with layers: {[layer.name for layer in merged_layers]}")
			

		# change volume of each layer
		# generate all of the semi-tones of each layer
		# mix all of the semi-tones of each layer (sox -m)
		#     if chord, mix for each chord
		#     if scale or arpeggio mix for each note
		# save to output folder and update instrument instructions

class Instrument:
	def __init__(self, name: str, key, mode, pan_value: PanValue, sounds: list[Sound]):
		self.name = name
		self.key = key
		self.mode = mode
		self.sounds = sounds
		self.pan_value = pan_value
		self.chords = []
		self.range = RANGE_IN_MODE[mode]
		self.notes_in_range = SCALE_INDEX_IN_MODE[mode]

	def __str__(self):
		return f"Instrument(name: {self.name}, key: {self.key}\nsounds:\n{self.sounds}\n)\n"
	def __repr__(self):
		return self.__str__()
	def __hash__(self) -> int:
		return hash(self.name)
	def __eq__(self, o: object) -> bool:
		if isinstance(o, Instrument):
			return self.name == o.name
		return False
	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)

	def get_pivot_filename(self, new_key, sound):
		for chord in self.chords:
			if chord.purpose == ChordPurpose.pivot and chord.key == new_key:
				return f"{self.name}_{sound.sound_type}_{chord.chord.name}.wav"

	# instrument.get_normal_filename(key, sound, note)
	# def get_normal_filename(self, key, sound, note):
	# 	# count how many layers have a tune
	# 	num_tonal_layers = 0
	# 	for layer in sound.layers:
	# 		if layer.note != Note.none:
	# 			num_tonal_layers += 1
	# 	seventh_chord = False
	# 	if num_tonal_layers >= 4:
	# 		seventh_chord = True

	# 	for chord in self.chords:
	# 		if chord.key == key:
	# 			if seventh_chord:
	# 				return f"{sound.name}_{chord.seventh_chord.name}_{note.name}.wav"
	# 			else:
	# 				return f"{sound.name}_{chord.chord.name}_{note.name}.wav"
			

	# get all the chords needed for this instrument, does not include seventh chords
	def set_chords(self, all_keys: list):
		chords = []
		# first chord for key
		for key in all_keys:
			chords.append(ChordClass(KEY_FIRST_CHORDS[key][0], ChordPurpose.normal, key))
		# pivot chords
		my_native_chords = KEY_NATIVE_CHORDS[self.key]
		for key in all_keys:
			if key != self.key:
				# find possible pivot chord
				their_native_chords = KEY_NATIVE_CHORDS[key]
				possible_pivot_chords = []
				for my_chord in my_native_chords:
					for their_chord in their_native_chords:
						if my_chord == their_chord and my_chord not in possible_pivot_chords:
							possible_pivot_chords.append(my_chord)
				# choose pivot chord whose CHORD_CLASSIFICATION is closest to the new key
				if len(possible_pivot_chords) > 0:
					for possible_pivot_chord in possible_pivot_chords:
						if CHORD_CLASSIFICATIONS[KEY_FIRST_CHORDS[key][0]] == CHORD_CLASSIFICATIONS[possible_pivot_chord]:
							chords.append(ChordClass(possible_pivot_chord, ChordPurpose.pivot, key))
							break
					else:
						chords.append(ChordClass(possible_pivot_chords[0], ChordPurpose.pivot, key))
				else:
					# no pivot chord found, use first chord
					chords.append(ChordClass(KEY_FIRST_CHORDS[key][0], ChordPurpose.pivot, key))
		self.chords = chords

	def generate_sounds(self):
		for sound in self.sounds:
			sound.generate(self)

def main():
	# validate arguments
	if len(sys.argv) < 2:
		print("Please provide a file name for the job")
		return
	# read jobfile
	jobfile_name = sys.argv[1]
	jobfile_lines = []
	with open(jobfile_name, "r") as f:
		jobfile_lines = f.readlines()

	# define job variables
	instruments = []
	most_recent_sound = None
	for i, line in enumerate(jobfile_lines):
		line_number = i + 1
		if line.startswith("instrument"):
			words = line.split(" ")
			# remove newline character from last word if it exists
			if words[-1].endswith("\n"):
				words[-1] = words[-1][:-1]

			if len(words) != 5:
				print(f"ERROR: line {line_number} of jobfile is not a valid instrument line")
				return
			
			new_instrument = Instrument(words[1], Key[words[2]], Mode[words[3]], PanValue(words[4]), [])
			if new_instrument in instruments:
				print(f"ERROR: instrument {new_instrument.name} is redefined in jobfile on line {line_number}")
				return
			instruments.append(new_instrument)
		elif line.startswith("sound"):
			words = line.split(" ")
			# remove newline character from last word if it exists
			if words[-1].endswith("\n"):
				words[-1] = words[-1][:-1]

			if len(words) != 3:
				print(f"ERROR: line {line_number} of jobfile is not a valid sound line")
				return
			sound_instrument = words[1]
			
			if sound_instrument not in [instrument.name for instrument in instruments]:
				print(f"ERROR: instrument {sound_instrument} is not defined in jobfile on line {line_number}")
				return
			sound_name = words[2]
			layers = []
			new_sound = Sound(sound_name, sound_instrument, layers)
			for instrument in instruments:
				if instrument.name == sound_instrument:
					if new_sound in instrument.sounds:
						print(f"ERROR: sound {new_sound.name} is redefined in jobfile on line {line_number}")
						return
					# print(f"Adding sound {new_sound.name} to instrument {instrument.name}")
					instrument.sounds.append(new_sound)
					break
			else:
				print(f"ERROR: sound {new_sound.name} is not defined in jobfile on line {line_number}")
				return
			most_recent_sound = new_sound
		elif line.startswith("-"):
			# add layer to sound
			words = line.split(" ")
			# remove newline character from last word if it exists
			if words[-1].endswith("\n"):
				words[-1] = words[-1][:-1]
			if len(words) != 4:
				print(f"ERROR: line {line_number} of jobfile is not a valid layer line")
				return
			if most_recent_sound is None:
				print(f"ERROR: layer line {line_number} of jobfile is not preceded by a sound line")
				return
			new_layer = Layer(words[1], Note[words[2]], float(words[3]))
			if new_layer in most_recent_sound.layers:
				print(f"ERROR: layer {new_layer.name} is redefined in jobfile on line {line_number}")
				return
			
			# print(f"Added layer {new_layer.name} to sound {most_recent_sound.name} of instrument {most_recent_sound.instrument_name}")
			most_recent_sound.layers.append(new_layer)

	# print("JOBFILE OUTPUT")
	# for instrument in instruments:
	# 	print(instrument)

	all_keys = [instrument.key for instrument in instruments]
	for instrument in instruments:
		instrument.set_chords(all_keys)

	# create tempory directory
	run_command(f"rm -r {TEMP_DIR}")
	run_command(f"mkdir {TEMP_DIR}")

	for instrument in instruments:
		print(f"Generating sounds for {instrument.name}...")
		instrument.generate_sounds()
	
	# gather all instrument instructions and write the tree to a file

# ote(note_i).name: instrument.get_normal_filename(key, sound, Note(note_i)) for note_i in SCALES[key]}
	instructions = {
		"key": {instrument.name: instrument.key.name for instrument in instruments},
		"range": {instrument.name: instrument.range for instrument in instruments},
		"pivot": {instrument.name: {sound.name.split("_")[0]: {key.name: instrument.get_pivot_filename(key, sound) for key in all_keys} for sound in instrument.sounds} for instrument in instruments},
		# TODO: make the notes from the scale go from lowest pitch to highest pitch
		# make the order of sounds in the capacitance layer be determined by the average note of the notes in the sound being in the centre of the capacitance layer
		"normal": {instrument.name: {sound.name.split("_")[0]: {key.name: sound.get_sound_filenames(instrument, key) for key in all_keys} for sound in instrument.sounds} for instrument in instruments},
	}

	# copy files at end of instructions

	# TODO export instructions
	# json_object = json.dumps(instructions, indent = 4) 
	# print(json_object)

	with open('instructions.json', 'w', encoding='utf-8') as f:
		json.dump(instructions, f, ensure_ascii=False, indent=4)

	output_filenames = []

	run_command(f"rm -r {OUTPUT_DIR}")
	run_command(f"mkdir {OUTPUT_DIR}")
	# wait a bit
	# time.sleep(1)
	# run_command(f"chmod 777 {TEMP_DIR}/*")
	stdout, stderr = run_command(f"ls {TEMP_DIR}")
	instrument_names = [instrument.name for instrument in instruments]
	for line in stdout.split("\n"):
		# if line starts with instrument names
		if line.startswith(tuple(instrument_names)):
			new_filename = line.split("_")
			del new_filename[2]
			new_filename = "_".join(new_filename)
			run_command(f"cp {TEMP_DIR}/{line} {OUTPUT_DIR}/{new_filename}")
			output_filenames.append(new_filename)
		# run_command(f"rsync {TEMP_DIR}/{instrument.name}*.wav {OUTPUT_DIR}")

	run_command(f"rm -r {TEMP_DIR}")

	cwd = os.getcwd()
	# check all filenames are in the output folder
	for instrument in instruments:
		for sound in instrument.sounds:
			for key in all_keys:
				pivot_filename = instrument.get_pivot_filename(key, sound)
				# check exists in output
				if not os.path.isfile(f"{cwd}/{OUTPUT_DIR}/{pivot_filename}") and pivot_filename:
					print(f"ERROR: File (pivot) not found in output directory: {pivot_filename}")
					exit()
				
				normal_filenames = sound.get_sound_filenames(instrument, key)
				for normal_filename in normal_filenames:
					# check exists in output
					if not os.path.isfile(f"{cwd}/{OUTPUT_DIR}/{normal_filename}"):
						print(f"ERROR: File (normal) not found in output directory: {normal_filename}")
						exit()

	# for filename in output_filenames:
	# 	# check exists in output
	# 	if not os.path.isfile(f"{cwd}/{OUTPUT_DIR}/{filename}"):
	# 		print(f"ERROR: File not found in output directory: {filename}")
	# 		exit()
				


	# display results
	print("========================================")
	print("GENERATED SOUNDS")
	print("----------------------------------------")
	print("Generated sounds")
	for instrument in instruments:
		print(f"{instrument.name}")
		for sound in instrument.sounds:
			print(f"    {sound.name}")

	print("----------------------------------------")
	print("FINISHED SUCCESSFULLY")
	print(f"Instructions: instructions.json")
	# state number of files in output directory
	stdout, stderr = run_command(f"ls {OUTPUT_DIR}")
	num_files = len(stdout.split("\n"))
	print(f"{num_files} files in output directory")
	print("========================================")

if __name__ == "__main__":
	main()