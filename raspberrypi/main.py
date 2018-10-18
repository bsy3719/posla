import server_connect
import rasp_serial
import Camera
import threading
import ultrasonic
import mic
import time

def run():
    HOST = '192.168.0.96'
    PORT = 5034
    #socket create for camera
    server_socket = server_connect.Connect(HOST, PORT)
    time.sleep(1)

    #socket create for ultrasonic sensor
    us_socket = server_connect.Connect(HOST, PORT+1)
    time.sleep(1)

    #socket create for mic
    mic_socket = server_connect.Connect(HOST, PORT+2)

    #create raspberrypi object
    serial = rasp_serial.Serial()    
    
    #if connected to server..start thread and send camera frame
    camera = Camera.Camera(server_socket.Get_Socket())
    camera_thread = threading.Thread(target=camera.run, args=())
    camera_thread.start()

    us = ultrasonic.UltraSonic()    
    us_thread = threading.Thread(target=us.run, args=(us_socket,))
    us_thread.start()

    microphone = mic.MicrophoneStream()    
    microphone_thread = threading.Thread(target=microphone.run, args=(mic_socket,))
    microphone_thread.start()

    print('start')

    while True:
        data =  server_socket.Get_Data()
        if data == 'q' :
            break
        serial.steer(data)
    
if __name__ == "__main__" :
    run()
