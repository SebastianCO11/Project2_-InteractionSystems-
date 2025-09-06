# src/game.py
from src.story import Story
from src.sound_manager import SoundManager

class Game:
    def __init__(self, debug=False):
        self.story = Story()
        self.sound_manager = SoundManager()
        self.running = True
        self.debug = debug

    def start(self):
        print("=== Bienvenido a la aventura del Laberinto ===")
        print("Tu objetivo es descubrir quién mató a tus padres...\n")

        # intenta arrancar música de fondo (silencia errores)
        try:
            self.sound_manager.play_background("ambient.wav", loop=True, gain=0.3)
        except Exception:
            pass

        # Bucle principal — implementado de forma explícita y segura
        while True:
            node = self.story.get_current()

            # DEBUG: información del nodo (id, choices, ending)
            if self.debug:
                choices_list = list(node.choices.keys())
                print(f"[DEBUG] node id={id(node)} ending={node.ending} choices={choices_list}")

            # Imprime el texto DEL NODO (una sola vez)
            print(node.text)

            # Reproduce sonido si existe
            if node.sound:
                try:
                    self.sound_manager.play(node.sound, node.position)
                except Exception:
                    pass

            # Si es final, mostramos la última línea (ya impresa) y terminamos
            if node.ending:
                print("\n=== Fin de la historia ===")
                break

            # Si solo hay 'Continuar' como única opción, hacemos auto-advance con Enter
            if node.choices and len(node.choices) == 1 and "Continuar" in node.choices:
                input("\nPresiona Enter para continuar...\n")
                moved = self.story.choose("Continuar")
                if not moved:
                    # fallback: forzar la transición si choose falla por alguna razón
                    target = list(node.choices.values())[0]
                    self.story.current = target
                continue

            # Si hay elecciones reales, muestro menú y espero número
            if node.choices:
                options = list(node.choices.keys())
                print("\nOpciones:")
                for i, option in enumerate(options, start=1):
                    print(f"{i}. {option}")

                # Bucle de entrada robusta
                while True:
                    choice = input("\nElige una opción: ").strip()
                    if not choice.isdigit():
                        print("Por favor escribe el número de la opción (ej: 1).")
                        continue
                    idx = int(choice) - 1
                    if idx < 0 or idx >= len(options):
                        print("Índice fuera de rango. Intenta de nuevo.")
                        continue
                    picked = options[idx]
                    break

                # Intentar elegir por el texto (método Story.choose)
                moved = self.story.choose(picked)
                if not moved:
                    # Fallback (forzar la transición si choose() no encuentra la clave)
                    try:
                        target = node.choices[picked]
                        # hack: accedemos y asignamos current (fall back interno)
                        self.story.current = target
                    except Exception as e:
                        print("[ERROR] No fue posible realizar la transición:", e)
                        print("Abortando juego para evitar estado inconsistente.")
                        break

                # Después de elegir, volvemos al inicio del bucle y mostraremos el nuevo nodo
                continue

            # Nodo sin choices y no final (no debería ocurrir con story bien formada)
            print("\n(No hay opciones; fin implícito.)")
            print("\n=== Fin de la historia ===")
            break

        # Limpieza audio
        try:
            self.sound_manager.stop_background()
            self.sound_manager.cleanup()
        except Exception:
            pass

from src.story import Story
from src.sound_manager import SoundManager

class Game:
    def __init__(self):
        self.story = Story()
        self.sound_manager = SoundManager()
        self.running = True

    def start(self):
        print("=== Bienvenido a la aventura del Laberinto ===")
        print("Tu objetivo es descubrir quién mató a tus padres...\n")

        self.sound_manager.play_background("ambient.wav", loop=True, gain=0.2)

        while self.running and not self.story.is_finished():
            node = self.story.get_current()
            print(node.text)

            if node.sound:
                self.sound_manager.play(node.sound, node.position)

            if node.ending:
                break

            if node.choices:
                print("\nOpciones:")
                for i, option in enumerate(node.choices.keys(), start=1):
                    print(f"{i}. {option}")

                choice = input("\nElige una opción: ")
                try:
                    choice_idx = int(choice) - 1
                    option = list(node.choices.keys())[choice_idx]
                    self.story.choose(option)
                except:
                    print("Opción inválida, intenta de nuevo.")
            else:
                input("\nPresiona Enter para continuar...\n")

        print("\n=== Fin de la historia ===")
