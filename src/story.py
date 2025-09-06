class StoryNode:
    def __init__(self, text, sound=None, position="center", choices=None, ending=False):
        self.text = text
        self.sound = sound
        self.position = position
        self.choices = choices if choices else {}
        self.ending = ending


def chain_lines(lines, ending=False):
    """
    lines = [(texto, sonido, posicion), ...]
    Devuelve (first, last) encadenando con 'Continuar'.
    Si ending=True, el último nodo se marca final y NO agrega 'Continuar'.
    """
    first = current = StoryNode(*lines[0])
    for line in lines[1:]:
        nxt = StoryNode(*line)
        current.choices = {"Continuar": nxt}
        current = nxt

    if ending:
        current.ending = True
        current.choices = {}  # nada de 'Continuar' si es final

    return first, current


class Story:
    def __init__(self):
        # --- INTRO ---
        intro_lines = [
            ("Despiertas frente a un laberinto colosal, cubierto de enredaderas y musgo.", "wind.wav", "left"),
            ("El aire es helado y una bruma espesa cubre la entrada.", "fog.wav", "front"),
            ("Sientes un escalofrío: una voz en tu mente susurra el recuerdo del asesinato de tus padres.", "whisper.wav", "back"),
            ("Sabes que solo entrando descubrirás la verdad.", "heartbeat.wav", "center")
        ]
        intro, final_intro = chain_lines(intro_lines)

        # --- OPCIONES DE ENTRADA ---
        puerta_lines = [
            ("Empujas la puerta de hierro y esta cruje como si nadie la hubiera abierto en siglos.", "door.wav", "front"),
            ("El eco metálico resuena por las paredes.", "echo.wav", "left"),
            ("El pasillo húmedo se bifurca en dos caminos: luz a la izquierda y oscuridad a la derecha.", "steps.wav", "front")
        ]
        puerta, final_puerta = chain_lines(puerta_lines)

        pasadizo_lines = [
            ("Rodeas los muros hasta encontrar un pasadizo cubierto de maleza.", "bush.wav", "right"),
            ("Te arrastras entre raíces húmedas y piedras afiladas que rasgan tu ropa.", "crawl.wav", "left"),
            ("El olor a tierra mojada y moho llena tus pulmones.", "cough.wav", "back"),
            ("Llegas a una sala amplia con estatuas antiguas y polvorientas.", "stone.wav", "front")
        ]
        pasadizo, final_pasadizo = chain_lines(pasadizo_lines)

        final_intro.choices = {
            "Entrar por la puerta principal": puerta,
            "Buscar otra entrada secreta": pasadizo
        }

        # --- RUTA A: PUERTA PRINCIPAL ---
        luz_lines = [
            ("Avanzas hacia la luz parpadeante.", "light.wav", "front"),
            ("Encuentras un mural tallado en piedra cubierto de grietas.", "mural.wav", "left"),
            ("Las letras rezan: 'La sangre llama a la sangre'.", "whisper2.wav", "center"),
            ("Un eco de pasos resuena detrás de ti, cada vez más cerca.", "steps2.wav", "back")
        ]
        luz, final_luz = chain_lines(luz_lines)

        oscuridad_lines = [
            ("Avanzas a ciegas entre sombras.", "dark.wav", "center"),
            ("Tropiezas con huesos dispersos en el suelo.", "bones.wav", "front"),
            ("Un susurro inhumano se desliza en tu oído: 'Fuiste tú… siempre fuiste tú'.", "whisper3.wav", "back")
        ]
        oscuridad, final_osc = chain_lines(oscuridad_lines)

        final_puerta.choices = {
            "Seguir la luz tenue": luz,
            "Adentrarte en la oscuridad profunda": oscuridad
        }

        # --- SUBRAMA A1: LUZ (no final; deriva a uno de los dos finales) ---
        esconderse_lines = [
            ("Te ocultas tras una columna cubierta de líquenes.", "hide.wav", "left"),
            ("Tus dedos tropiezan con un papel húmedo.", "paper.wav", "front"),
            ("Al abrirlo, ves tu nombre escrito con tinta roja.", "note.wav", "right"),
            ("El mensaje dice: 'Él sabe la verdad'.", "whisper4.wav", "back")
        ]
        esconderse, end_esconderse = chain_lines(esconderse_lines, ending=False)

        enfrentar_lines = [
            ("Te giras con valentía, y una sombra femenina se materializa.", "shadow.wav", "front"),
            ("Sus ojos brillan en la penumbra.", "eyes.wav", "left"),
            ("Una voz grave te llama: 'Hijo… no debiste volver'.", "voice.wav", "back"),
            ("El aire se enfría como si hubieras invocado a un espectro.", "cold.wav", "center")
        ]
        enfrentar, end_enfrentar = chain_lines(enfrentar_lines, ending=False)

        final_luz.choices = {
            "Esconderte": esconderse,
            "Enfrentar la presencia": enfrentar
        }

        # --- SUBRAMA A2: OSCURIDAD → convergen al FINAL 'TÚ' ---
        negar_lines = [
            ("Avanzas tambaleante y encuentras un espejo roto apoyado contra la pared.", "mirror.wav", "front"),
            ("Tu reflejo sonríe con manchas de sangre en el rostro.", "laugh.wav", "center")
        ]
        negar, end_negar = chain_lines(negar_lines, ending=False)

        recordar_lines = [
            ("Imágenes dolorosas revientan en tu mente.", "memory1.wav", "front"),
            ("Una mano sosteniendo un cuchillo… tu propia mano.", "knife.wav", "left"),
            ("Los gritos de tus padres resuenan como un eco lejano.", "scream.wav", "back"),
            ("El calor de la sangre en tus dedos te quiebra.", "blood.wav", "center")
        ]
        recordar, end_recordar = chain_lines(recordar_lines, ending=False)

        # Final único "TÚ"
        self_final_lines = [
            ("Comprendes con horror la verdad innegable: tú mismo los mataste.", "truth.wav", "front")
        ]
        self_final, _ = chain_lines(self_final_lines, ending=True)

        # Convergencia a final "TÚ"
        end_negar.choices = {"Aceptar la verdad": self_final}
        end_recordar.choices = {"Asumir la culpa": self_final}

        final_osc.choices = {
            "Negarlo y seguir": negar,
            "Recordar lo que pasó": recordar
        }

        # --- RUTA B: PASADIZO (no final; deriva a TÚ o MADRE) ---
        estatuas_lines = [
            ("Te acercas a una estatua agrietada.", "statue.wav", "front"),
            ("Lees con esfuerzo la inscripción: 'Ella lo ocultó todo'.", "engraving.wav", "left"),
            ("Dentro de una grieta descubres un collar dorado.", "collar.wav", "center"),
            ("Lo reconoces al instante: pertenecía a tu madre.", "gasp.wav", "back")
        ]
        estatuas, end_estatuas = chain_lines(estatuas_lines, ending=False)

        tunel_lines = [
            ("Sigues un túnel lateral donde un llanto femenino retumba.", "cry1.wav", "front"),
            ("Cada paso hace que el lamento sea más intenso.", "cry2.wav", "left"),
            ("Al final del túnel, una puerta se abre sola con un chirrido.", "door2.wav", "back"),
            ("Dentro, ves a tu madre arrodillada, llorando.", "mother.wav", "front")
        ]
        tunel, final_tunel = chain_lines(tunel_lines)

        final_pasadizo.choices = {
            "Revisar las estatuas": estatuas,
            "Seguir un túnel lateral": tunel
        }

        # --- SUBRAMA B2: MADRE → convergen al FINAL 'MADRE' ---
        acercarte_lines = [
            ("Te aproximas temblando.", "step.wav", "front"),
            ("Ella toma tu mano con desesperación.", "grip.wav", "left"),
            ("'Hijo… fui yo quien hizo esto… perdóname'.", "confession.wav", "back")
        ]
        acercarte, end_acercarte = chain_lines(acercarte_lines, ending=False)

        escuchar_lines = [
            ("Permanece oculto en las sombras mientras ella solloza.", "sob.wav", "front"),
            ("En el suelo encuentras una carta arrugada.", "paper.wav", "left"),
            ("La lees: 'No tuve elección… yo fui quien acabó con todo'.", "letter.wav", "back")
        ]
        escuchar, end_escuchar = chain_lines(escuchar_lines, ending=False)

        # Final único "MADRE"
        mother_final_lines = [
            ("Sientes el peso de su confesión: fue tu madre quien los mató.", "cry2.wav", "center")
        ]
        mother_final, _ = chain_lines(mother_final_lines, ending=True)

        # Convergencia a final "MADRE"
        end_acercarte.choices = {"Abrazarla y perdonarla": mother_final}
        end_escuchar.choices = {"Aceptar lo leído": mother_final}

        final_tunel.choices = {
            "Acercarte a tu madre": acercarte,
            "Escuchar en silencio": escuchar
        }

        # --- Convergencias desde rutas no finales ---
        # Desde LUZ (esconderse / enfrentar) puedes ir hacia sombras (TÚ) o llanto (MADRE)
        end_esconderse.choices = {
            "Seguir las sombras": oscuridad,
            "Seguir el llanto": tunel
        }
        end_enfrentar.choices = {
            "Seguir las sombras": oscuridad,
            "Seguir el llanto": tunel
        }

        # Desde ESTATUAS te llevo a decidir hacia cuál gran final ir
        end_estatuas.choices = {
            "Seguir el llanto": tunel,
            "Regresar a la oscuridad": oscuridad
        }

        # Estado inicial
        self.current = intro

    def get_current(self):
        return self.current

    def choose(self, option):
        if option in self.current.choices:
            self.current = self.current.choices[option]
            return True
        return False

    def is_finished(self):
        return self.current.ending
