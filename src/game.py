import os
from src.story import Story
from src.sound_manager import SoundManager


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def print_text_box(lines):
    width = max(len(line) for line in lines) + 2
    print("╔" + "═" * width + "╗")
    for line in lines:
        print(f"║ {line.ljust(width - 1)}║")
    print("╚" + "═" * width + "╝")


def show_start_screen():
    clear_console()
    try:
        with open("resources/ascii_title.txt", "r", encoding="utf-8") as f:
            ascii_title = f.read()
        print(ascii_title)
    except Exception:
        print("[TITLE ART MISSING]")
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
            self.sound_manager.listener.set_orientation((0, 0, 1, 0, 1, 0))
            self.sound_manager.play_background("ambient.wav", loop=True, volume=0.3)
            show_start_screen()
            print("Your goal is to discover who killed your parents...\n")
        except Exception:
            pass

        while True:
            node = self.story.get_current()

            clear_console()

            if self.debug:
                choices_list = list(node.choices.keys())
                print(f"[DEBUG] node id={id(node)} ending={node.ending} choices={choices_list}")

            print_text_box([node.text])

            if node.sound:
                try:
                    self.sound_manager.play(node.sound, node.position)
                except Exception:
                    pass

            if node.ending:
                print("\n=== End of story ===")
                break

            if node.choices and len(node.choices) == 1 and "Continuar" in node.choices:
                input("Presiona Enter para continuar...\n")
                moved = self.story.choose("Continuar")
                if not moved:
                    target = list(node.choices.values())[0]
                    self.story.current = target
                continue

            if node.choices:
                options = list(node.choices.keys())
                print_text_box([f"{i+1}) {op}" for i, op in enumerate(options)])

                while True:
                    choice = input("\nChoose an option: ").strip()
                    if not choice.isdigit():
                        print("Por favor selecciona una opción.")
                        continue
                    idx = int(choice) - 1
                    if idx < 0 or idx >= len(options):
                        print("Number out of range. Try again.")
                        continue
                    picked = options[idx]
                    break

                moved = self.story.choose(picked)
                if not moved:
                    try:
                        target = node.choices[picked]
                        self.story.current = target
                    except Exception as e:
                        print(f"[ERROR] Could not advance: {e}")
                        break
                continue

            print("\n(No options; implicit end.)")
            print("\n=== End of story ===")
            break

        try:
            self.sound_manager.stop_background()
            self.sound_manager.cleanup()
        except Exception:
            pass
