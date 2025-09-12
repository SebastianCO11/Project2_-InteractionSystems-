from openal import oalOpen, Listener
import threading


class SoundManager:
    def __init__(self):
        self.listener = Listener()
        self.listener.set_position((0, 0, 0))
        self.listener.set_orientation((0, 0, 1, 0, 1, 0))

        self.master_volume = 1.0
        self.background_volume = 0.2
        self.sfx_volume = 3.0

        self.background = None
        self.current_sfx = None

    def set_master_volume(self, volume: float):
        self.master_volume = max(0.0, min(1.0, volume))
        if self.background:
            self.background.set_gain(self.background_volume * self.master_volume)
        if self.current_sfx:
            self.current_sfx.set_gain(self.sfx_volume * self.master_volume)

    def set_background_volume(self, volume: float):
        self.background_volume = max(0.0, min(1.0, volume))
        if self.background:
            self.background.set_gain(self.background_volume * self.master_volume)

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))
        if self.current_sfx:
            self.current_sfx.set_gain(self.sfx_volume * self.master_volume)

    def play_background(self, filename, loop=True, volume=None):
        def _play_bg():
            try:
                if self.background:
                    self.background.stop()
                    self.background = None

                snd = oalOpen(f"sounds/{filename}")
                if loop:
                    snd.set_looping(True)

                if volume is not None:
                    self.background_volume = max(0.0, min(1.0, volume))
                snd.play()
                snd.set_gain(
                    self.background_volume * self.master_volume
                )
                self.background = snd
            except Exception as e:
                print(f"[Error in background music {filename}] {e}")

        threading.Thread(target=_play_bg, daemon=True).start()

    def stop_background(self):
        if self.background:
            self.background.stop()
            self.background = None

    def play(self, filename, position="center", gain=None, exclusive=True):
        def _play():
            try:
                if exclusive and self.current_sfx:
                    self.current_sfx.stop()

                snd = oalOpen(f"sounds/{filename}")

                if position == "left":
                    snd.set_position((-10, 0, 0))
                elif position == "right":
                    snd.set_position((10, 0, 0))
                elif position == "back":
                    snd.set_position((0, 0, -10))
                elif position == "front":
                    snd.set_position((0, 0, 10))
                else:
                    snd.set_position((0, 0, 0))

                eff = self.sfx_volume if gain is None else max(0.0, min(1.0, gain))
                snd.play()
                snd.set_gain(eff * self.master_volume)

                self.current_sfx = snd
            except Exception as e:
                print(f"[Error reproduciendo {filename}] {e}")

        threading.Thread(target=_play, daemon=True).start()
