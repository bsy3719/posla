import server_socket
import threading

class Microphone(object):

    def __init__(self, host, port, steer):
        
        self.steer = steer
        self.socket = server_socket.Server(host, port)
        self.client = self.socket.Get_Client()
    

    def Recv(self) :
        while True :
            speech = self.client.recv(128).decode()
            print('speech', speech)
            self.steer.Set_Microphone(speech)
    
    def Run(self) :
        mic_thread = threading.Thread(target=self.Recv, args=())
        mic_thread.start()

    
