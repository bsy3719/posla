''' pg_midi_sound101.py
play midi music files (also mp3 files) using pygame
tested with Python273/331 and pygame192 by vegaseat
'''
#code modified from here: https://www.daniweb.com/programming/software-development/code/454835/let-pygame-play-your-midi-or-mp3-files


#raspberry-pi setup
#https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage

#GPIO Pin
#18, 19, 21 used and they CAN NOT CAHNGE!(Fixed Pin)

#!/usr/bin/python

#import sys
import pygame as pg
import os
import time

#print('speech : ', (transcript + overwirte_chars))
class MUSIC():
    def __init__(self, volume = 1.0, freq = 44100, bitsize = -16, channels = 2, buffer = 2048):
        self.volume = volume
        self.freq = freq    # audio CD quality
        self.bitsize = bitsize   # unsigned 16 bit
        self.channels = channels    # 1 is mono, 2 is stereo
        self.buffer = buffer   # number of samples (experiment to get right sound)
        pg.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)
        # optional volume 0 to 1.0
        pg.mixer.music.set_volume(self.volume)        

    def play_music(self, music_file):
        '''
        CrashSamp.mp3stream music with mixer.music module in blocking manner
        this will stream the sound from disk while playing
        '''

        while pg.mixer.music.get_busy() == True :
            return

        try:
            pg.mixer.music.load(music_file)
            print("Music file {} loaded!".format(music_file))
        except pygame.error:
            print("File {} not found! {}".format(music_file, pg.get_error()))
            return

        pg.mixer.music.play()
