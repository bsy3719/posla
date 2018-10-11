import server_connect
import rasp_serial
import Camera
import threading

def run():
    HOST = '192.168.0.90'
    PORT = 5034
    server = server_connect.Connect(HOST, PORT)
    serial = rasp_serial.Serial()    
    
    camera = Camera.Camera(server.Get_Socket())
    camera_thread = threading.Thread(target=camera.run, args=())
    camera_thread.start()

    print('start')

    while True:
        data =  server.Get_Data()
        if data == 'q' :
            break
        serial.steer(data)
    
if __name__ == "__main__" :
    run()
