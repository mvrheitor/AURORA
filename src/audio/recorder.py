import sounddevice as sd
import numpy as np
import threading

class Gravador:
    def __init__(self, samplerate=44100):
        self.samplerate = samplerate
        self.frames = []
        self.gravando = False

    def iniciar(self):
        self.frames = []
        self.gravando = True
        self.thread = threading.Thread(target=self._gravar)
        self.thread.start()

    def parar(self):
        self.gravando = False
        self.thread.join()
        return np.concatenate(self.frames, axis=0)

    def _gravar(self): # _ antes da função significa que ela não deve ser chamada fora da classe (é uma convenção em python)
        with sd.InputStream(samplerate=self.samplerate, channels=1, dtype="int16") as stream:
            while self.gravando:
                data, _ = stream.read(1024)
                self.frames.append(data.copy())
