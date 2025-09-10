# src/game.py
import os
from src.story import Story
from src.sound_manager import SoundManager


def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")


def cuadro_texto(lineas):
    """
    Recibe una lista de strings y los imprime dentro de un cuadro ASCII.
    """
    ancho = max(len(linea) for linea in lineas) + 2  # padding interno
    print("╔" + "═" * ancho + "╗")
    for linea in lineas:
        print(f"║ {linea.ljust(ancho - 1)}║")
    print("╚" + "═" * ancho + "╝")


def pantalla_inicio():
    limpiar_consola()
    ascii_title = r"""
██       ▄   ▄███▄      ▄     ▄▄▄▄▀ ▄   █▄▄▄▄ ██       ▄███▄      ▄       ▄███▄   █         █    ██   ███   ▄███▄   █▄▄▄▄ ▄█    ▄     ▄▄▄▄▀ ████▄     
█ █       █  █▀   ▀      █ ▀▀▀ █     █  █  ▄▀ █ █      █▀   ▀      █      █▀   ▀  █         █    █ █  █  █  █▀   ▀  █  ▄▀ ██     █ ▀▀▀ █    █   █     
█▄▄█ █     █ ██▄▄    ██   █    █  █   █ █▀▀▌  █▄▄█     ██▄▄    ██   █     ██▄▄    █         █    █▄▄█ █ ▀ ▄ ██▄▄    █▀▀▌  ██ ██   █    █    █   █     
█  █  █    █ █▄   ▄▀ █ █  █   █   █   █ █  █  █  █     █▄   ▄▀ █ █  █     █▄   ▄▀ ███▄      ███▄ █  █ █  ▄▀ █▄   ▄▀ █  █  ▐█ █ █  █   █     ▀████     
   █   █  █  ▀███▀   █  █ █  ▀    █▄ ▄█   █      █     ▀███▀   █  █ █     ▀███▀       ▀         ▀   █ ███   ▀███▀     █    ▐ █  █ █  ▀                
  █     █▐           █   ██        ▀▀▀   ▀      █              █   ██                              █                 ▀       █   ██                   
 ▀      ▐                                      ▀                                                  ▀                                                                                                                                       
"""
    print(ascii_title)
    print("Presiona ENTER para iniciar")
    input()


class Game:
    def __init__(self, debug=False):
        self.story = Story()
        self.sound_manager = SoundManager()
        self.running = True
        self.debug = debug

    def start(self):
        try:
            self.sound_manager.play_background("ambient.wav", loop=True, gain=0.3)
            pantalla_inicio()
            print("Tu objetivo es descubrir quién mató a tus padres...\n")
        except Exception:
            pass

        while True:
            node = self.story.get_current()

            limpiar_consola()  # Limpia pantalla antes de mostrar

            if self.debug:
                choices_list = list(node.choices.keys())
                print(
                    f"[DEBUG] node id={id(node)} ending={node.ending} choices={choices_list}"
                )

            # Texto del nodo
            cuadro_texto([node.text])

            # Sonido
            if node.sound:
                try:
                    self.sound_manager.play(node.sound, node.position)
                except Exception:
                    pass

            if node.ending:
                print("\n=== Fin de la historia ===")
                break

            if node.choices and len(node.choices) == 1 and "Continuar" in node.choices:
                input("\nPresiona Enter para continuar...\n")
                moved = self.story.choose("Continuar")
                if not moved:
                    target = list(node.choices.values())[0]
                    self.story.current = target
                continue

            if node.choices:
                opciones = list(node.choices.keys())
                cuadro_texto([f"{i+1}) {op}" for i, op in enumerate(opciones)])

                while True:
                    choice = input("\nElige una opción: ").strip()
                    if not choice.isdigit():
                        print("Por favor escribe el número de la opción.")
                        continue
                    idx = int(choice) - 1
                    if idx < 0 or idx >= len(opciones):
                        print("Número fuera de rango. Intenta de nuevo.")
                        continue
                    picked = opciones[idx]
                    break

                moved = self.story.choose(picked)
                if not moved:
                    try:
                        target = node.choices[picked]
                        self.story.current = target
                    except Exception as e:
                        print("[ERROR] No fue posible avanzar:", e)
                        break
                continue

            print("\n(No hay opciones; fin implícito.)")
            print("\n=== Fin de la historia ===")
            break

        try:
            self.sound_manager.stop_background()
            self.sound_manager.cleanup()
        except Exception:
            pass
