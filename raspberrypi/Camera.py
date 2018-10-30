import io
import struct
import time
import picamera

class Camera(object):
    def __init__(self, server):
        self.server = server.makefile('wb')

    def run(self):
        with picamera.PiCamera() as camera :
            camera.resolution = (320, 240)
            camera.framerate = 20
            time.sleep(2)
            start = time.time()
            stream = io.BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port = True) :
                self.server.write(struct.pack('<L', stream.tell()))
                self.server.flush()
                stream.seek(0)
                self.server.write(stream.read())
                if time.time() - start > 600 :
                    break
                stream.seek(0)
                stream.truncate()
        self.server.write(struct.pack('<L', 0))
