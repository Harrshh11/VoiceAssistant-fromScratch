import pvporcupine
import pyaudio
import struct
from enginee.command import allCommands  

def start_hotword_detection():
    porcupine = pvporcupine.create(keywords=["hey siri"])
    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for hotword 'Hey Siri'...")

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Hotword detected!")
            allCommands()  #  Directly call the function from command.py
