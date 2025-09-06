# test_spatial.py
import time
from openal import oalOpen, Listener

# Crear al "jugador" (oyente) en el centro
listener = Listener()
listener.set_position((0, 0, 0))
listener.set_orientation((0, 0, 1, 0, 1, 0))  # mirando hacia adelante

def play_with_position(filename, position, seconds=3):
    """Reproduce un sonido en una posición 3D por unos segundos"""
    sound = oalOpen(f"sounds/{filename}")
    sound.set_position(position)
    sound.set_reference_distance(1)   # volumen máximo hasta 1 unidad
    sound.set_rolloff_factor(1)       # qué tan rápido baja el volumen
    sound.set_max_distance(50)        # distancia máxima
    sound.play()
    print(f"▶ Reproduciendo {filename} en {position} durante {seconds}s")
    time.sleep(seconds)
    sound.stop()

if __name__ == "__main__":
    # Cambia este nombre por un archivo que tengas en sounds/
    test_file = "step.wav"

    play_with_position(test_file, (-10, 0, 0))  # izquierda
    play_with_position(test_file, (10, 0, 0))   # derecha
    play_with_position(test_file, (0, 0, 10))   # adelante
    play_with_position(test_file, (0, 0, -10))  # atrás

    print("✅ Prueba de espacialidad finalizada")
