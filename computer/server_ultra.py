import server_socket
import threading

class UltraSonic(object):

    def __init__(self, host, port, steer):
        
        self.steer = steer
        self.socket = server_socket.Server(host, port)
        self.client = self.socket.Get_Client()

    def Recv(self) :
        while True : 
            distance = self.client.recv(64).decode()  
            self.steer.Set_UltraSonic(distance)         
    
    def Run(self) :
        us_thread = threading.Thread(target=self.Recv, args=())
        us_thread.start()

