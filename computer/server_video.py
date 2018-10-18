import numpy as np
import cv2
import threading

import Object
import StopLine

from model import NeuralNetwork

class CollectTrainingData(object):

    def __init__(self, client, steer):        

        self.client = client        
        self.steer = steer

        self.stopline = StopLine.Stop()
        self.dect = Object.Object_Detection()

        # model create
        self.model = NeuralNetwork()
        self.model.load_model(path = 'training_data/video_model_1.h5')          

    def collect(self):

        print("Start video stream")        

        stream_bytes = b' '  
 
        while True :            
            stream_bytes += self.client.recv(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')

            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]

                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                rgb = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)   
                roi = image[120:240, :]

                
                cv2.imshow('RGB', rgb)
                cv2.imshow('GRAY', image)
                cv2.imshow('roi', roi)

                # reshape the roi image into a vector
                image_array = np.reshape(roi, (-1, 120, 320, 1))                  

                try:
                    # neural network makes prediction
                    self.steer.Set_Line(self.model.predict(image_array))
                    print(self.stopline.GetStopLine(rgb))
                    self.steer.Set_ObjectDectection(self.dect.Dectection(rgb))                    
                    self.steer.Control()
                except:
                    continue

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break




























