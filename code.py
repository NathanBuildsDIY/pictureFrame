"""
DIY Talking Picture Frame
"""
import board
import audiomp3
import audiopwmio
import os
import time
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import pwmio

#get all mp3 to play
phrases = [f for f in os.listdir('.') if f.endswith('.mp3')]
#set up audio output - thank you https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
audio = audiopwmio.PWMAudioOut(board.GP0)
# LED setup.
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False
# button setup
button = DigitalInOut(board.GP16)
button.switch_to_input(pull=Pull.UP)
button_state = 1
prev_button_state = 1

#modulo cycle through mp3s
index = 0

while True:
  time.sleep(0.1) #power saving
  prev_button_state = button_state
  button_state = button.value
  if prev_button_state != button_state:
    time.sleep(0.3) # Debounce delay
  if prev_button_state == 1 and button_state == 0:
    #detected initial click - toggle values
    led.value = True
    phrase = phrases[index % len(phrases)]
    print(phrase) #print file that we'll play
    decoder = audiomp3.MP3Decoder(open(phrase, "rb"))
    audio.play(decoder)
    while audio.playing:
      pass
    led.value = False
    index = index + 1

print("Done playing!")