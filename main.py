import serial
import pygame

PRESSED = True
UNPRESSED = False

TICKS_PER_SECOND = 30

PLANT = 0
WATER = 1
LIGHT = 2
FABRIC = 3

# To change which input plays which sound, modify this list
# The first input plays SOUNDS[0], second SOUNDS[1], etc.
SOUNDS_PATH = ['sounds/plant.wav', 'sounds/water.wav', 'sounds/light.wav', 'sounds/fabric.wav']

pygame.init()
plant_sound1 = pygame.mixer.Sound('Sounds/plant.wav')
water_sound1 = pygame.mixer.Sound('Sounds/water.wav')
light_sound1 = pygame.mixer.Sound('Sounds/light.wav')
fabric_sound1 = pygame.mixer.Sound('Sounds/fabric.wav')
guitar_sound1 = pygame.mixer.Sound('Sounds/short-guitar-riff.wav')

plant_sound2 = pygame.mixer.Sound('Sounds/plant.wav')
water_sound2 = pygame.mixer.Sound('Sounds/water.wav')
light_sound2 = pygame.mixer.Sound('Sounds/light.wav')
fabric_sound2 = pygame.mixer.Sound('Sounds/fabric.wav')
guitar_sound2 = pygame.mixer.Sound('Sounds/short-guitar-riff.wav')

SOUNDS1 = [light_sound1, plant_sound1, water_sound1, guitar_sound1, fabric_sound1]
SOUNDS2 = [light_sound2, plant_sound2, water_sound2, guitar_sound2, fabric_sound2]

SOUNDS_COMBINED = []
SOUNDS_COMBINED.extend(SOUNDS1)
SOUNDS_COMBINED.extend(SOUNDS2)



clock = pygame.time.Clock()

def get_serial():

        #run to get port on MacOs 'ls -l /dev/cu.usb*'
        sPort1 = '/dev/cu.usbserial-10'
        ser1 = serial.Serial(sPort1, 9600, timeout=1)
        data1 = ser1.readline()

        sPort2 = '/dev/cu.usbmodem1101'
        ser2 = serial.Serial(sPort2, 9600, timeout=1)
        data2 = ser2.readline()

        states = []
        playing = [True, True, True, True, True, True, True, True, True, True]
        threads = []
        thresholds = [800, 200, 200, 200, 200, 800, 200, 200, 200, 200]

        records = []
        recording = False
        records_size = 0
        record_start_time = 0

        play_rec = False
        play_index = 0
        play_start_time = 0

        parsed_data = None
        parsed_data1 = None
        parsed_data2 = None

        while True:

            ticks = pygame.time.get_ticks()
            #print(ticks)

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        recording = not recording
                        if recording:
                            record_start_time = ticks
                            print("recording started")
                        else:
                            print((ticks - record_start_time)/1000)
                            print("recording stopped")
                            records_size = len(records)

                    if event.key == pygame.K_s:
                        play_rec = not play_rec
                        if play_rec:
                            play_start_time = ticks
                            print("playing started")
                        else:
                            print("playing stopped")

            if ser1.inWaiting() > 0:
                # Read data from serial
                data1 = ser1.readline()
                parsed_data1 = data1.decode().strip().split(" ")
                #print("arduino 1: ", parsed_data1)

            if ser2.inWaiting() > 0:
                # Read data from serial
                data2 = ser2.readline()
                parsed_data2 = data2.decode().strip().split(" ")
                #print("arduino 2: ", parsed_data2)

            if parsed_data1 and parsed_data2:
                #    print("arduino 1: ", parsed_data1, "arduino 2: ", parsed_data2)
                parsed_data = list()
                parsed_data.extend(parsed_data1)
                parsed_data.extend(parsed_data2)
                print(parsed_data)

            if recording:
                records.append(parsed_data)

            if play_rec:
                if play_index < records_size:
                    parsed_data = records[play_index]
                elif play_index == records_size:
                    print("playing finished")
                    play_rec = False
                    print((ticks - play_start_time) / 1000)
                play_index += 1

            if parsed_data:
                # Check that thread and state lists are correct size
                while len(parsed_data) > len(states):
                    states.append(UNPRESSED)
                while len(parsed_data) > len(threads):
                    threads.append(None)

                # Start a new thread to play the sound for each input
                for i in range(len(parsed_data)):
                    value = int(parsed_data[i])

                    if (value > thresholds[i] or value == -2) and states[i] != PRESSED:
                        states[i] = PRESSED

                        if i == LIGHT:
                            playing[i] = (playing[i] != True)
                            if not playing[i]:
                                SOUNDS_COMBINED[i].play(loops=-1)
                            else:
                                SOUNDS_COMBINED[i].stop()

                        elif i != LIGHT:
                            SOUNDS_COMBINED[i].play(loops=-1)

                for i in range(len(parsed_data)):
                    value = int(parsed_data[i])
                    if (value <= thresholds[i] and value != -2) and states[i] == PRESSED:
                        states[i] = UNPRESSED

                        if i != LIGHT:
                            SOUNDS_COMBINED[i].stop()

            clock.tick(TICKS_PER_SECOND * 3)


if __name__ == '__main__':


    #x = Process(target=get_serial, args=())
    #x.start()

    get_serial()


