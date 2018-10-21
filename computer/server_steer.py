import server_socket
import threading
import os
import time

class Steer(object):

    def __init__(self, client):
        self.client = client
        self.ultrasonic = 0
        self.microphone = ''
        self.line = ''
        self.obj_list = []
        self.stopline = False
        self.state = ''
        
    def Set_UltraSonic(self, ultra) :
        self.ultrasonic = int(ultra)

    def Set_Microphone(self, mic) :
        self.microphone = mic

    def Set_Line(self, line) :
        self.line = line

    def Set_Stopline(self, result):
        self.stopline = result

    def Set_ObjectDetection(self, obj) :
        self.obj_list = obj

    def ultrasonic_process(self, ultra) :
        if ultra < 20 :
            return 's' 
        else :
            return 'w'

    def mic_process(self, speech) :
        if (speech == '정지') or (speech == '멈춰') :
            return 's'  
        elif (speech == '가') or (speech == '가라고') or (speech == '출발') :
            return 'w'
        else :
            return ''

    def Control(self) :
        mic_comm = self.mic_process(self.microphone)
        us_comm = self.ultrasonic_process(self.ultrasonic)

        #os.system('clear')
        print('전방 거리 : ', self.ultrasonic)
        print('상태 : ', self.state)
        print('음성 명령 : ', self.microphone)

        # all station only one send data
        # speed limit
        if 'limit30' in self.obj_list :
            if self.state != '30' :
                self.client.send('30'.encode())
                self.state = '30'
        elif 'limit60' in self.obj_list :
            print('limit 60')
            if self.state != '60' :
                self.client.send('60'.encode())
                self.state = '60'

        # stop 
        # it's only for different sound..
        if ('redlight' in self.obj_list) and (self.stopline == True) :
            if (self.state != 'STOP') or (mic_comm == 'w') :
                self.state = 'STOP'
                self.client.send('ls'.encode())
                print('RED LIGHT')

        elif (mic_comm == 's') :
            if self.state != 'STOP' :
                self.client.send('s'.encode())
                self.state = 'STOP'
                print('STOP')

        elif (us_comm == 's') :
            if self.state != 'STOP' :
                self.client.send('us'.encode())
                self.state = 'STOP'
                print('STOP')

        # driving
        else :  
            if self.state != 'RUN' :          
                self.state = 'RUN'
                if ('turn_right_yes' in self.obj_list) and (self.stopline == True) : 
                    time.sleep(1)
                    self.client.send('d'.encode())
                elif self.line == 2:                
                    self.client.send('w'.encode())
                    print("FORWARD")
                elif self.line == 0:
                    self.client.send('a'.encode())
                    print("LEFT")
                elif self.line == 1:
                    self.client.send('d'.encode())
                    print("RIGHT")
                else :
                    print("WAIT..")

        self.microphone = ''
