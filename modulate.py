from instrument import Instrument

class Modulator:
	"""
	Static class to modulate all instruments to a new key
	"""
	def modulate(old_key: str, new_key: str, all_instruments: list[Instrument], modulating_instrument: Instrument) -> None:
		"""
		Static function to modulate all instruments to the given key
		Parameters:
			new_key: the key to modulate to
			all_instruments: a list of all instruments
		"""
		print(f"MODULATING TO {new_key}")
		# play pivot chord
		pivot_sound = modulating_instrument.sound_objects["pivot"][modulating_instrument.name]["impact"][old_key]
		print(f"+ {modulating_instrument.name} playing PIVOT CHORD {pivot_sound}")
		pivot_sound.play()
		# change all other instruments to the new key
		for instrument in all_instruments:
			# if the instrument is currently playing, stop it and play it again in the new key
			if instrument._currently_playing:
				instrument.stop()
				instrument.play(new_key, False)