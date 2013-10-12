from __future__ import division
import pyaudio

RATE = 44100
CHUNK = 1024
SECONDS = 3
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32, channels=2, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = [stream.read(CHUNK) for i in xrange(int(RATE / CHUNK * SECONDS))]

stream.stop_stream()
stream.close()
p.terminate()
