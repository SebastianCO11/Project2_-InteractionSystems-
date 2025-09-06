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
