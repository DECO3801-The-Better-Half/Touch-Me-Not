import sys
import subprocess
import random
import json 
import time
import os
from constants import *

reduce_volume_warnings = []
command_count = 0
def run_command(command: str, use_shell = False) -> tuple[str, str]:
	"""
	Runs a command and returns the output and error
	"""
	global command_count
	command_count += 1

	process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=use_shell)
	stdout, stderr = process.communicate()
	# decode bytes to string
	stdout = stdout.decode("utf-8")
	stderr = stderr.decode("utf-8")
	if stderr:
		for ignored_warning in IGNORED_WARNINGS:
			if ignored_warning in stderr:
				break
		else:
			print(f"---ERROR from subprocess---\n{command}\n---------------------------\n\n{stderr}\n\n---End of ERROR from subprocess---\nExiting...")
			exit()
	return stdout, stderr

class PanValue:
	"""
	Represents a pan value for a sound
	"""
	def __init__(self, pan_description: str):
		"""
		Parameters:
			pan_description: a string of the form "LxRy" where x and y are floats
		"""
		self.pan_description = pan_description
		self.left = float(pan_description.split("R")[0][1:])
		self.right = float(pan_description.split("R")[1])

class Layer:
	"""
	Represents a layer of a sound
	"""

	def __init__(self, file_address: str, note, volume_sf: float):
		"""
		Parameters:
			file_address: the address of the file
			note: the note of the file
			volume_sf: the volume scale factor of the file
		"""
		self.file_address = file_address
		self.name = file_address.split("/")[-1].split(".")[0]
		self.temp_file_address = f"{TEMP_DIR}/{self.name}.wav"
		self.temp_file_address_no_extension = f"{TEMP_DIR}/{self.name}"
		self.note = note
		self.note_number = note.value
		self.volume_sf = volume_sf

	def get_address_for_note(self, note: Note):
		"""
		Returns the address of the file for the given note
		Parameters:
			note: the note to get the address for
		"""
		# print(note)
		if self.note == Note.none:
			return self.temp_file_address
		# print(f"{self.temp_file_address_no_extension}_{note.name}.wav")
		return f"{self.temp_file_address_no_extension}_{note.name}.wav"

	def copy_to_temp_dir(self):
		"""
		Copies the file to the temp directory
		"""
		run_command(f"cp {self.file_address} {self.temp_file_address}")

	def change_wav_volume(self):
		"""
		Changes the volume of the wav file
		"""
		# create temporary file
		run_command(f"cp {self.temp_file_address} {self.temp_file_address_no_extension}_temp.wav")
		run_command(f"rm {self.temp_file_address}")
		# use temporary file to change volume
		run_command(f"sox -v {self.volume_sf} {self.temp_file_address_no_extension}_temp.wav {self.temp_file_address}")
		# delete temporary file
		run_command(f"rm {self.temp_file_address_no_extension}_temp.wav")

	def change_wav_pan(self, pan_value: PanValue):
		"""
		Changes the pan of the wav file
		Parameters:
			pan_value: the pan value to change to
		"""
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
		"""
		Generates all the notes for the layer
		"""
		if self.note == Note.none:
			return
		for note_number in range(0, 12):
			new_note = Note[Note(note_number).name] #I'm sure this is not how its supposed to be done
			new_file_address = self.get_address_for_note(new_note)
			pitch_value = ((new_note.value - self.note.value + NUM_PITCH_DOWNS) % 12 - NUM_PITCH_DOWNS) * 100
			run_command(f"sox {self.temp_file_address} {new_file_address} pitch {pitch_value}")

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

class ChordClass:
	"""
	Represents a chord class
	"""
	def __init__(self, chord, purpose, key = None):
		"""
		Parameters:
			chord: the chord
			purpose: the purpose of the chord
			key: the key of the chord
		"""
		self.chord = chord # Chord
		self.seventh_chord = Chord[f"{chord.name}_seventh"]
		self.purpose = purpose # ChordPurpose
		self.key = key # If purpose is pivot, this is the key of the pivot chord, if purpose is normal, this is the key of the chord
	

class Sound:
	"""
	Represents a sound
	"""
	def __init__(self, name: str, instrument_name: str, layers: list, volume_sf: float = 1.0):
		"""
		Parameters:
			name: the name of the sound
			instrument_name: the name of the instrument
			layers: the layers of the sound
		"""
		self.name = name + "_" + instrument_name
		self.sound_type = name
		self.layers = layers
		self.instrument_name = instrument_name
		self.volume_sf = volume_sf

	def num_tonal_layers(self):
		"""
		Returns the number of tonal layers
		"""
		return len([layer for layer in self.layers if layer.note != Note.none])

	def get_sound_filenames(self, instrument: 'Instrument', key):
		"""
		Returns the sound filenames for the sound
		Parameters:
			instrument: the instrument
			key: the key of the sound
		"""
		sound_filenames = []
		# if chord add key first chord
		if instrument.mode == Mode.chord:
			# add key chord
			sound_filenames.append(f"{instrument.name}_{self.sound_type}_{key.name}.wav")
		# if arpeggio or scale add key arpeggio notes
		elif instrument.mode == Mode.arpeggio or instrument.mode == Mode.scale:
			# adds chord anyway
			sound_filenames.append(f"{instrument.name}_{self.sound_type}_{key.name}.wav")
			for note_number in SCALE_INDEX_IN_MODE[instrument.mode]:
				note = SCALES[key][note_number]
				sound_filenames.append(f"{instrument.name}_{self.sound_type}_{note.name}.wav")

		return sound_filenames

	def change_wav_volume(self, filename: str):
		"""
		Changes the volume of the wav file
		"""
		# create temporary file
		run_command(f"cp {filename} {filename}_temp.wav")
		run_command(f"rm {filename}")
		# use temporary file to change volume
		run_command(f"sox -v {self.volume_sf} {filename}_temp.wav {filename}")
		# delete temporary file
		run_command(f"rm {filename}_temp.wav")


	def merge_layer(self, new_sound_address, new_layer_address):
		"""
		Merges the layer into the sound
		Parameters:
			new_sound_address: the address of the new sound
			new_layer_address: the address of the new layer
		"""
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

	def generate(self, instrument: 'Instrument'):
		"""
		Generates the sound
		Parameters:
			instrument: the instrument of the sound
		"""
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
				# change the volume_sf of the sound
				self.change_wav_volume(new_sound_address)
				# print(f"CREATING: {instrument.name} {self.name} note: {new_note.name}")

		# generate all the chords
		for chord in instrument.chords:
			# this can be removed to generate fewer files, though it was requested that it was not
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
				if i == 0:
					run_command(f"cp {layer.get_address_for_note(closest_note)} {new_sound_address}")
				else:
					self.merge_layer(new_sound_address, layer.get_address_for_note(closest_note))
				merged_layers.append(layer)
			# change the volume_sf of the sound
			self.change_wav_volume(new_sound_address)
	
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


class Instrument:
	"""
	Instrument class
	"""
	def __init__(self, name: str, key, mode, pan_value: PanValue, sounds: list[Sound]):
		"""
		Parameters:
			name: name of the instrument
			key: key of the instrument
			mode: mode of the instrument
			pan_value: pan value of the instrument
			sounds: list of Sound objected of the instrument
		"""
		self.name = name
		self.key = key
		self.mode = mode
		self.sounds = sounds
		self.pan_value = pan_value
		self.chords = []
		self.range = RANGE_IN_MODE[mode]
		self.notes_in_range = SCALE_INDEX_IN_MODE[mode]

	def get_pivot_filename(self, new_key, sound):
		"""
		Returns the filename of the pivot sound
		Parameters:
			new_key: the new key of the instrument
			sound: the sound to get the pivot filename for
		"""
		for chord in self.chords:
			if chord.purpose == ChordPurpose.pivot and chord.key == new_key:
				return f"{self.name}_{sound.sound_type}_{chord.chord.name}.wav"

	def set_chords(self, all_keys: list):
		"""
		Sets the chords of the instrument. Does not include seventh chords.
		Parameters:
			all_keys: list of all the keys
		"""
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
		"""
		Generates the sounds of the instrument
		"""
		for sound in self.sounds:
			sound.generate(self)

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

def main():
	"""
	Main function.
	Parses jobfile, generates layers for all pitches, generates sounds for all needed keys, 
	saves them to output folder along with instructions file.
	"""
	start_time = time.time()
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

			if len(words) != 4:
				print(f"ERROR: line {line_number} of jobfile is not a valid sound line")
				return
			sound_instrument = words[1]
			sound_volume_sf = 1
			try:
				sound_volume_sf = float(words[3])
			except ValueError:
				print(f"ERROR: line {line_number} of jobfile has invalid volume_sf")
				return
			
			if sound_instrument not in [instrument.name for instrument in instruments]:
				print(f"ERROR: instrument {sound_instrument} is not defined in jobfile on line {line_number}")
				return
			sound_name = words[2]
			layers = []
			new_sound = Sound(sound_name, sound_instrument, layers, sound_volume_sf)
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
			most_recent_sound.layers.append(new_layer)

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
	instructions = {
		"key": {instrument.name: instrument.key.name for instrument in instruments},
		"range": {instrument.name: instrument.range for instrument in instruments},
		"pivot": {instrument.name: {sound.name.split("_")[0]: {key.name: instrument.get_pivot_filename(key, sound) for key in all_keys} for sound in instrument.sounds} for instrument in instruments},
		# make the order of sounds in the capacitance layer be determined by the average note of the notes in the sound being in the centre of the capacitance layer
		"normal": {instrument.name: {sound.name.split("_")[0]: {key.name: sound.get_sound_filenames(instrument, key) for key in all_keys} for sound in instrument.sounds} for instrument in instruments},
	}
	with open('instructions.json', 'w', encoding='utf-8') as f:
		json.dump(instructions, f, ensure_ascii=False, indent=4)
	output_filenames = []

	run_command(f"rm -r {OUTPUT_DIR}")
	run_command(f"mkdir {OUTPUT_DIR}")
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
	stdout, stderr = run_command(f"ls {OUTPUT_DIR}")
	num_files = len(stdout.split("\n"))
	print(f"{num_files} files in output directory")
	print(f"{command_count} commands run\n{time.time() - start_time} seconds")
	print("========================================")

if __name__ == "__main__":
	main()