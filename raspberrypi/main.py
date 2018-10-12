import server_connect
import rasp_serial
import Camera
import threading
import ultrasonic

def run():
    HOST = '192.168.0.90'
    PORT = 5034
    #socket create for camera
    camera_socket = server_connect.Connect(HOST, PORT)
    
    #socket create for ultrasonic sensor
    #us_socket = server_connect.Connect(HOST, PORT+1)
    
    #create raspberrypi object
    serial = rasp_serial.Serial()    
    
    #if connected to server..start thread and send camera frame
    camera = Camera.Camera(camera_socket.Get_Socket())
    camera_thread = threading.Thread(target=camera.run, args=())
    camera_thread.start()

    #us = ultrasonic.UltraSonic()    
    #us_thread = threading.Thread(target=us.run, args=(us_socket,))
    #us_thread.start()

    print('start')

    while True:
        data =  server.Get_Data()
        if data == 'q' :
            break
        serial.steer(data)
    
if __name__ == "__main__" :
    run()
