from webCamStream import webCamStream

class camStream:
    def __init__(self, src=0, usePiCam=False, resolution=(320, 240), framerate=32):
        
        if usePiCam:
            from rpiCamStream import rpiCamStream
            self.stream = rpiCamStream(resolution=resolution, framerate=framerate)
        
        else:
            self.stream = webCamStream(src=src)
    
    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()

    def read(self):
        return self.stream.read()

    def stop(self):
        self.stream.stop()
