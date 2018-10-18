import server_socket
import threading
import os

class Steer(object):

    def __init__(self, client):
        self.client = client
        self.ultrasonic = 0.
        self.microphone = ''
        self.line = ''
        self.obj_list = []
        
    def Set_UltraSonic(self, ultra) :
        self.ultrasonic = float(ultra)

    def Set_Microphone(self, mic) :
        self.microphone = mic

    def Set_Line(self, line) :
        self.line = line

    def Set_ObjectDectection(self, obj) :
        self.obj_list = obj

    def ultrasonic_process(self, ultra) :
        if ultra < 30. :
            return 's' 
        else :
            return 'w'

    def mic_process(self, speech) :
        if speech == '멈춰' :
            return 's'
        elif speech == '가' :
            return 'w'
        elif speech == '가라고' :
            return 'w'
 

    def Control(self) :               
        us_comm = self.ultrasonic_process(self.ultrasonic)
        print('dis', us_comm, self.ultrasonic)

        mic_comm = self.mic_process(self.microphone)
        print('음성 명령 :: ', mic_comm)
        
        if (mic_comm == 's') :
            self.client.send('s'.encode())
        else :
            if self.line == 2:                
                self.client.send('w'.encode())
                print("Forward")
            elif self.line == 0:
                self.client.send('a'.encode())
                print("Left")
            elif self.line == 1:
                self.client.send('d'.encode())
                print("Right")
            else :
                print("None")
             
