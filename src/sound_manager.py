from openal import oalOpen, Listener
import threading


class SoundManager:
    def __init__(self):
        # Listener (por si luego quieres mover orientación/posición)
        self.listener = Listener()
        self.listener.set_position((0, 0, 0))
        self.listener.set_orientation((0, 0, 1, 0, 1, 0))  # mira hacia +Z

        # Volúmenes por tipo
        self.master_gain = 1.0
        self.bg_gain = 0.2  # volumen por defecto del ambiente
        self.sfx_gain = 3.0  # volumen por defecto de efectos

        # Referencias a sonidos activos
        self.background = None
        self.current_sfx = None

    # ---------- helpers de volumen ----------
    def set_master_volume(self, gain: float):
        """0.0–1.0 (aplica multiplicador a todo)"""
        self.master_gain = max(0.0, min(1.0, gain))
        # aplica inmediatamente a lo que esté sonando
        if self.background:
            self.background.set_gain(self.bg_gain * self.master_gain)
        if self.current_sfx:
            self.current_sfx.set_gain(self.sfx_gain * self.master_gain)

    def set_background_volume(self, gain: float):
        """0.0–1.0 (solo ambiente)"""
        self.bg_gain = max(0.0, min(1.0, gain))
        if self.background:  # 🔥 aplica en caliente
            self.background.set_gain(self.bg_gain * self.master_gain)

    def set_sfx_volume(self, gain: float):
        """0.0–1.0 (solo efectos)"""
        self.sfx_gain = max(0.0, min(1.0, gain))
        if self.current_sfx:
            self.current_sfx.set_gain(self.sfx_gain * self.master_gain)

    # ---------- reproducción ----------
    def play_background(self, filename, loop=True, gain=None):
        """Música de fondo (se reemplaza si ya había una)"""

        def _bg():
            try:
                # si hay uno sonando, lo paramos
                if self.background:
                    self.background.stop()
                    self.background = None

                snd = oalOpen(f"sounds/{filename}")
                if loop:
                    snd.set_looping(True)

                # aplica volumen efectivo (bg_gain * master_gain)
                if gain is not None:
                    self.bg_gain = max(0.0, min(1.0, gain))
                snd.play()
                snd.set_gain(
                    self.bg_gain * self.master_gain
                )  # 👈 aplica después de play
                self.background = snd
            except Exception as e:
                print(f"[Error en música de fondo {filename}] {e}")

        threading.Thread(target=_bg, daemon=True).start()

    def stop_background(self):
        if self.background:
            self.background.stop()
            self.background = None

    def play(self, filename, position="center", gain=None, exclusive=True):
        """Efecto puntual. exclusive=True corta el anterior."""

        def _play():
            try:
                if exclusive and self.current_sfx:
                    self.current_sfx.stop()

                snd = oalOpen(f"sounds/{filename}")

                # posición 3D
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

                # volumen efectivo del sfx
                eff = self.sfx_gain if gain is None else max(0.0, min(1.0, gain))
                snd.play()
                snd.set_gain(eff * self.master_gain)  # aplica después de play

                self.current_sfx = snd
            except Exception as e:
                print(f"[Error reproduciendo {filename}] {e}")

        threading.Thread(target=_play, daemon=True).start()
