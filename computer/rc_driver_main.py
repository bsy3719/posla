import server_video
import server_ultra
import server_microphone
import server_steer
import server_socket

import threading

if __name__ == '__main__':
    # host, port
    host, port = "192.168.0.96", 5034

    client = server_socket.Server(host, port)

    steer = server_steer.Steer(client.Get_Client()) 

    ultrasonic_object = server_ultra.UltraSonic(host, port+1, steer)
    ultrasonic_object.Run()
    
    microphone_object = server_microphone.Microphone(host, port+2, steer)
    microphone_object.Run()

    # loop
    video_object = server_video.CollectTrainingData(client.Get_Client(), steer)
    video_object.collect()
