import numpy as np
import sounddevice as sd
import time
import threading

class AudioMonitor:
    def __init__(self, update_interval=0.05):
        self.update_interval = update_interval
        self.current_volume = 0.0
        self.is_running = False
        self._thread = None
        self._stream = None

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
        if self._thread:
            self._thread.join(timeout=1)

    def _audio_callback(self, indata, frames, time_info, status):
        # Calculate RMS amplitude
        volume_norm = np.linalg.norm(indata) * 10
        self.current_volume = min(volume_norm, 100.0)

    def _monitor_loop(self):
        try:
            self._stream = sd.InputStream(callback=self._audio_callback, channels=1, samplerate=44100)
            with self._stream:
                while self.is_running:
                    time.sleep(self.update_interval)
        except Exception as e:
            print(f"[AudioMonitor] Error: {e}")
            self.is_running = False

    def get_volume(self):
        return self.current_volume
