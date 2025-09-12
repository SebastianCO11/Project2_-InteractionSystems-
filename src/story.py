class StoryNode:
    def __init__(self, text, sound=None, position="center", choices=None, ending=False):
        self.text = text
        self.sound = sound
        self.position = position
        self.choices = choices if choices else {}
        self.ending = ending


def chain_lines(lines, ending=False):
    first = current = StoryNode(*lines[0])
    for line in lines[1:]:
        nxt = StoryNode(*line)
        current.choices = {"Continuar": nxt}
        current = nxt

    if ending:
        current.ending = True
        current.choices = {}

    return first, current


class Story:
    def __init__(self):
        self.history = []

    # --- INTRO ---
        intro_lines = [
            (
                "Despiertas frente a un laberinto colosal cubierto de enredaderas y musgo; el cielo gris parece a punto de desplomarse.",
                "forest.wav",
                "left",
            ),
            (
                "El aire es helado, y una bruma espesa cubre la entrada con un olor metálico.",
                "fog.wav",
                "front",
            ),
            (
                "Sientes un escalofrío: una voz en tu mente susurra el recuerdo del asesinato de tus padres.",
                "whisper.wav",
                "back",
            ),
            (
                "El suelo bajo tus pies cruje; sabes que solo entrando descubrirás la verdad.",
                "heartbeat.wav",
                "center",
            ),
        ]
        intro, final_intro = chain_lines(intro_lines)

    # --- ENTRY OPTIONS ---
        puerta_lines = [
            (
                "Empujas la puerta de hierro; cruje como si nadie la hubiera abierto en siglos.",
                "door.wav",
                "front",
            ),
            (
                "El eco metálico se propaga; tu respiración es el único sonido vivo.",
                "echo.wav",
                "left",
            ),
            (
                "El pasillo húmedo se bifurca: luz parpadeante a la izquierda, oscuridad absoluta a la derecha.",
                "steps.wav",
                "front",
            ),
            (
                "Sientes que alguien te observa desde las sombras; tu respiración se corta.",
                "breathe.wav",
                "back",
            ),
        ]
        puerta, final_puerta = chain_lines(puerta_lines)

        pasadizo_lines = [
            (
                "Rodeas los muros cubiertos de musgo hasta hallar un pasadizo cubierto de maleza.",
                "bush.wav",
                "right",
            ),
            (
                "Te arrastras entre raíces húmedas y piedras afiladas; tu ropa se rasga.",
                "crawl.wav",
                "left",
            ),
            (
                "El olor a tierra mojada y moho es tan intenso que te mareas.",
                "cough.wav",
                "back",
            ),
            (
                "Emerges en una sala amplia con estatuas antiguas, sus ojos de piedra parecen seguirte.",
                "stone.wav",
                "front",
            ),
        ]
        pasadizo, final_pasadizo = chain_lines(pasadizo_lines)

        final_intro.choices = {
            "Entrar por la puerta principal": puerta,
            "Buscar otra entrada secreta": pasadizo,
        }

    # --- ROUTE A: MAIN DOOR ---
        luz_lines = [
            (
                "Avanzas hacia la luz parpadeante; cada paso hace crujir el suelo de madera podrida.",
                "light.wav",
                "front",
            ),
            (
                "Un mural tallado en piedra muestra figuras humanas con rostros borrados.",
                "mural.wav",
                "left",
            ),
            (
                "Unas letras rezan: 'La sangre llama a la sangre'.",
                "whisper2.wav",
                "center",
            ),
            (
                "Un eco de pasos resuena detrás de ti; tu corazón late tan fuerte que casi ensordece.",
                "steps2.wav",
                "back",
            ),
        ]
        luz, final_luz = chain_lines(luz_lines)

        oscuridad_lines = [
            (
                "Avanzas a ciegas; el aire es tan espeso que tragar duele.",
                "dark.wav",
                "center",
            ),
            (
                "Tropiezas con huesos húmedos dispersos en el suelo.",
                "bones.wav",
                "front",
            ),
            (
                "Un olor a hierro viejo llena el pasillo, y un susurro roza tu oído: 'Fuiste tú… siempre fuiste tú'.",
                "whisper3.wav",
                "back",
            ),
            (
                "Sientes dedos helados rozando tu cuello; das un salto y el silencio vuelve.",
                "touch.wav",
                "back",
            ),
        ]
        oscuridad, final_osc = chain_lines(oscuridad_lines)

        final_puerta.choices = {
            "Seguir la luz tenue": luz,
            "Adentrarte en la oscuridad profunda": oscuridad,
        }

    # --- SUB-BRANCH A1: LIGHT ---
        esconderse_lines = [
            (
                "Te ocultas tras una columna cubierta de líquenes; apenas respiras.",
                "hide.wav",
                "left",
            ),
            ("Tus dedos tropiezan con un papel húmedo.", "paper.wav", "front"),
            (
                "Al abrirlo, ves tu nombre escrito con tinta roja; la caligrafía es familiar.",
                "note.wav",
                "right",
            ),
            ("El mensaje dice: 'Él sabe la verdad'.", "whisper4.wav", "back"),
        ]
        esconderse, end_esconderse = chain_lines(esconderse_lines)

        mural_extra_lines = [
            (
                "Observas de cerca el mural: una figura central lleva una máscara dorada.",
                "mask.wav",
                "center",
            ),
            (
                "Notas una llave oxidada escondida en una grieta; decides guardarla.",
                "key.wav",
                "left",
            ),
        ]
        mural_extra, _ = chain_lines(mural_extra_lines)

        enfrentar_lines = [
            (
                "Te giras con valentía: una sombra femenina se materializa.",
                "shadow.wav",
                "front",
            ),
            (
                "Sus ojos brillan como carbones en la penumbra; su cabello flota sin viento.",
                "eyes.wav",
                "left",
            ),
            ("Una voz grave retumba: 'Hijo… no debiste volver'.", "voice.wav", "back"),
            (
                "El aire se enfría de golpe, tu aliento es visible; la presencia parece disfrutar tu miedo.",
                "low_rumble.wav",
                "center",
            ),
        ]
        enfrentar, end_enfrentar = chain_lines(enfrentar_lines)

        final_luz.choices = {
            "Esconderte": esconderse,
            "Examinar el mural": mural_extra,
            "Enfrentar la presencia": enfrentar,
        }

    # --- SUB-BRANCH A2: DARKNESS ---
        negar_lines = [
            (
                "Encuentras un espejo roto apoyado en la pared; apenas refleja tu silueta.",
                "mirror.wav",
                "front",
            ),
            (
                "Tu reflejo sonríe con manchas de sangre en el rostro.",
                "laugh.wav",
                "center",
            ),
            ("Sientes que el espejo late al ritmo de tu corazón.", "pulse.wav", "back"),
        ]
        negar, end_negar = chain_lines(negar_lines)

        recordar_lines = [
            (
                "Recuerdos estallan en tu mente; gritos ahogados, sangre en las paredes.",
                "whisper_reverse.wav",
                "front",
            ),
            ("Una mano sosteniendo un cuchillo… tu propia mano.", "knife.wav", "left"),
            (
                "El aliento cálido de tu madre pidiéndote que pares.",
                "scream_female.wav",
                "back",
            ),
            ("Tus dedos aún recuerdan el calor de la sangre.", "blood.wav", "center"),
        ]
        recordar, end_recordar = chain_lines(recordar_lines)

        self_final_lines = [
            (
                "La verdad es innegable: fuiste tú quien asesinó a tus padres.",
                "truth.wav",
                "front",
            )
        ]
        self_final, _ = chain_lines(self_final_lines, ending=True)

        end_negar.choices = {"Aceptar la verdad": self_final}
        end_recordar.choices = {"Asumir la culpa": self_final}

        final_osc.choices = {
            "Negarlo y seguir": negar,
            "Recordar lo que pasó": recordar,
        }

    # --- ROUTE B: PASSAGE ---
        estatuas_lines = [
            (
                "Te acercas a una estatua agrietada; sus ojos parecen moverse.",
                "statue.wav",
                "front",
            ),
            (
                "Lees: 'Ella lo ocultó todo'; la inscripción está manchada de algo oscuro.",
                "engraving.wav",
                "left",
            ),
            (
                "Dentro de una grieta descubres un collar dorado.",
                "collar.wav",
                "center",
            ),
            ("Lo reconoces: pertenecía a tu madre.", "gasp.wav", "back"),
        ]
        estatuas, end_estatuas = chain_lines(estatuas_lines)

        tunel_lines = [
            (
                "Sigues un túnel lateral; un llanto femenino retumba.",
                "cry1.wav",
                "front",
            ),
            (
                "Cada paso lo intensifica; sientes que algo camina detrás de ti.",
                "cry2.wav",
                "left",
            ),
            (
                "Al final del túnel, una puerta se abre sola con un chirrido prolongado.",
                "door2.wav",
                "back",
            ),
            (
                "Dentro, ves a tu madre arrodillada, llorando en silencio.",
                "mother.wav",
                "front",
            ),
        ]
        tunel, final_tunel = chain_lines(tunel_lines)

        final_pasadizo.choices = {
            "Revisar las estatuas": estatuas,
            "Seguir un túnel lateral": tunel,
        }

    # --- SUB-BRANCH B2: MOTHER ---
        acercarte_lines = [
            (
                "Te aproximas temblando; ella levanta el rostro bañado en lágrimas.",
                "steps.wav",
                "front",
            ),
            ("Ella toma tu mano con fuerza; su piel está helada.", "grip.wav", "left"),
            ("'Hijo… fui yo quien hizo esto… perdóname'.", "confession.wav", "back"),
        ]
        acercarte, end_acercarte = chain_lines(acercarte_lines)

        escuchar_lines = [
            (
                "Permanece oculto en las sombras; sus sollozos son cuchillas.",
                "sob.wav",
                "front",
            ),
            (
                "Encuentras una carta arrugada: 'No tuve elección… yo acabé con todo'.",
                "letter.wav",
                "back",
            ),
        ]
        escuchar, end_escuchar = chain_lines(escuchar_lines)

        mother_final_lines = [
            (
                "El peso de la confesión te aplasta: tu madre mató a tu padre… y a ti te dejó vivo.",
                "cry2.wav",
                "center",
            )
        ]
        mother_final, _ = chain_lines(mother_final_lines, ending=True)

        end_acercarte.choices = {"Abrazarla y perdonarla": mother_final}
        end_escuchar.choices = {"Aceptar lo leído": mother_final}

        final_tunel.choices = {
            "Acercarte a tu madre": acercarte,
            "Escuchar en silencio": escuchar,
        }

    # --- NEW ROUTES AND ENDINGS ---
        guardian_lines = [
            (
                "El suelo tiembla; del techo cae polvo mientras una figura gigantesca emerge.",
                "guardian.wav",
                "front",
            ),
            (
                "Su rostro es una máscara sin ojos; sostiene una espada oxidada.",
                "sword.wav",
                "center",
            ),
            (
                "'Eres el último de tu estirpe', resuena en tu mente.",
                "voice2.wav",
                "back",
            ),
        ]
        guardian, end_guardian = chain_lines(guardian_lines)

        guardian_final_lines = [
            (
                "El Guardián del Laberinto te atraviesa con su espada; tu historia termina en el olvido.",
                "death.wav",
                "front",
            )
        ]
        guardian_final, _ = chain_lines(guardian_final_lines, ending=True)

        end_guardian.choices = {"Aceptar tu destino": guardian_final}

        father_lines = [
            (
                "En una sala oculta ves a tu padre vivo; su mirada está llena de odio.",
                "father.wav",
                "front",
            ),
            (
                "'Todo esto lo hice para protegerte', susurra, antes de apuntarte con un arma.",
                "gun.wav",
                "back",
            ),
        ]
        father, end_father = chain_lines(father_lines)

        father_final_lines = [
            (
                "Un disparo retumba; tu padre cae muerto. Tú eres ahora el guardián del secreto.",
                "shot.wav",
                "center",
            )
        ]
        father_final, _ = chain_lines(father_final_lines, ending=True)

        escape_lines = [
            (
                "Corres sin mirar atrás, atravesando puertas y pasadizos.",
                "run.wav",
                "front",
            ),
            (
                "El frío te persigue, pero logras salir al bosque. Jamás sabrás la verdad.",
                "forest.wav",
                "center",
            ),
        ]
        escape, _ = chain_lines(escape_lines, ending=True)

    # --- EXTRA CONNECTIONS ---
        end_esconderse.choices = {
            "Seguir las sombras": oscuridad,
            "Seguir el llanto": tunel,
            "Explorar un ruido extraño": guardian,
        }
        end_enfrentar.choices = {
            "Seguir las sombras": oscuridad,
            "Seguir el llanto": tunel,
            "Escapar corriendo": escape,
        }
        end_estatuas.choices = {
            "Seguir el llanto": tunel,
            "Regresar a la oscuridad": oscuridad,
            "Forzar una puerta oculta": father,
        }

        self._intro = intro
        self.current = intro

    # --- Interaction Methods ---
    def get_current(self):
        return self.current

    def get_choices(self):
        return list(self.current.choices.keys())

    def choose(self, option):
        if option in self.current.choices:
            self.history.append((self.current.text, option))
            self.current = self.current.choices[option]
            return True
        return False

    def is_finished(self):
        return self.current.ending

    def restart(self):
        self.current = self._intro
        self.history = []

    def get_path(self):
        lines = ["CAMINO RECORRIDO\n"]
        for i, (text, choice) in enumerate(self.history, 1):
            lines.append(f"{i}. {text}\n   Elegiste: {choice}\n")
        lines.append(f"FINAL: {self.current.text}")
        return "\n".join(lines)
