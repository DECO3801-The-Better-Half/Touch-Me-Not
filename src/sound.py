"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys

NUM_FILES = 2

if len(sys.argv) < NUM_FILES + 1:
    print(f"Plays a wave file.\n\nUsage: {sys.argv[0]} "
          f"{'filename.wav' * NUM_FILES}")
    sys.exit(-1)

wfs = [
    wave.open(sys.argv[1], 'rb'),
    wave.open(sys.argv[2], 'rb'),
]

# instantiate PyAudio (1)
p = pyaudio.PyAudio()


# define callback (2)
def callback1(in_data, frame_count, time_info, status):
    data = wfs[0].readframes(frame_count)
    if len(data) / 3 < frame_count:
        print(len(data), frame_count, time_info, status)
    return (data, pyaudio.paContinue)


def callback2(in_data, frame_count, time_info, status):
    data = wfs[1].readframes(frame_count)
    if len(data) / 3 < frame_count:
        print(len(data), frame_count, time_info, status)
    return (data, pyaudio.paContinue)


# open stream using callback (3)
streams = []
streams.append(
    p.open(format=p.get_format_from_width(wfs[0].getsampwidth()),
           channels=wfs[0].getnchannels(),
           rate=wfs[0].getframerate(),
           output=True,
           stream_callback=callback1)
)
streams.append(
    p.open(format=p.get_format_from_width(wfs[1].getsampwidth()),
           channels=wfs[1].getnchannels(),
           rate=wfs[1].getframerate(),
           output=True,
           stream_callback=callback2)
)

# start the stream (4)
for stream in streams:
    stream.start_stream()

# wait for stream to finish (5)
# while stream.is_active():
#     time.sleep(0.1)

while True:
    activations = [stream.is_active() for stream in streams]
    if True not in activations:
        break
    else:
        time.sleep(0.1)

# stop stream (6)
for i in range(NUM_FILES):
    streams[i].stop_stream()
    streams[i].close()
    wfs[i].close()

# close PyAudio (7)
p.terminate()
