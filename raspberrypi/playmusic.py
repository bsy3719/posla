import pygame as pg
import os
import time

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

        while pg.mixer.music.get_busy() == True :
            return

        try:
            pg.mixer.music.load(music_file)
            print("Music file {} loaded!".format(music_file))
        except pygame.error:
            print("File {} not found! {}".format(music_file, pg.get_error()))
            return

        pg.mixer.music.play()
