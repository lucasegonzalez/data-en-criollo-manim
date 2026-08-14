"""Skyline 3D — Las 12 torres mas altas del mundo (Data en Criollo).

Showcase de MANIM 3D + CAMARA: un skyline de rascacielos a escala real
(metros/100). La camara establece, orbita suave, vuela por encima de la
ciudad (sweep), se centra en la torre heroica, y cierra con el "money shot"
desde arriba. Todo el texto es fixed-in-frame (nada de texto en 3D), sin
intersecciones (cero z-fighting), sin duotono, un solo acento terracota.

Run (mp4 con audio):
  ~/miniforge3/envs/manim/bin/manim render -q m torres_3d.py TorresSkyline3D
"""

import os

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_expo, smooth
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_COL = os.path.join(BASE, "assets/blip_col.wav")
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

# (nombre, metros, x, y, color, ancho) — altura real / 100 = unidades
TOWERS = [
    ("LOTTE WORLD", 555, -3.9, 1.5, TINTA_MED, 0.66),
    ("PING AN", 599, -1.3, 1.5, OLIVA, 0.66),
    ("TIANJIN CTF", 530, 1.3, 1.5, TINTA_MED, 0.66),
    ("CITIC TOWER", 528, 3.9, 1.5, OLIVA, 0.66),
    ("MERDEKA 118", 679, -3.9, 0.0, MOSTAZA, 0.66),
    ("BURJ KHALIFA", 828, -1.3, 0.0, TERRACOTA, 0.55),
    ("SHANGHAI TOWER", 632, 1.3, 0.0, MOSTAZA, 0.66),
    ("ONE WORLD TRADE", 541, 3.9, 0.0, STEEL, 0.66),
    ("ABRAJ AL-BAIT", 601, -3.9, -1.5, STEEL, 0.66),
    ("SHANGHAI WFC", 492, -1.3, -1.5, PAPEL2, 0.66),
    ("GUANGZHOU CTF", 530, 1.3, -1.5, PAPEL2, 0.66),
    ("TAIPEI 101", 509, 3.9, -1.5, STEEL, 0.66),
]

Z_PISO = 0.03
ESCALA = 100.0  # 1 unidad = 100 metros

# Torre heroica: Burj Khalifa, 828 m
HERO_NOMBRE = "BURJ KHALIFA · DUBAI"
HERO_DATO = "828 METROS — EL PRIMERO EN ROMPER LOS 800"


def altura(t):
    return t[1] / ESCALA


def footprint(t):
    _, m, x, y, color, w = t
    f = Prism(
        dimensions=(w + 0.1, w + 0.1, 0.03),
        fill_color=CREMA,  # socket visible sobre la plataforma
        fill_opacity=1,
        stroke_color=color,
        stroke_width=3,
    )
    f.move_to([x, y, Z_PISO / 2])
    return f


def torre(t):
    _, m, x, y, color, w = t
    h = altura(t)
    col = Prism(
        dimensions=(w, w, h),
        fill_color=color,
        fill_opacity=0.95,
        stroke_color=TINTA,
        stroke_width=4,
    )
    col.move_to([x, y, Z_PISO + h / 2])
    return col


class TorresSkyline3D(ThreeDScene):
    def construct(self):
        # --- Fondo paper grain + plataforma (diorama de papel) ---
        self.camera.background_color = PAPEL
        fondo = ImageMobject(os.path.join(BASE, "assets/papel_grain.png"))
        fondo.scale(2.6).move_to([0, 0, -35])
        fondo.set_opacity(0.45)  # textura visible sin gritar (estatica)
        self.add(fondo)

        plataforma = Prism(
            dimensions=(13.4, 7.4, 0.14),
            fill_color=PAPEL2,
            fill_opacity=1,
            stroke_color=TINTA,
            stroke_width=2,
        )
        plataforma.move_to([0, 0, -0.07])
        self.add(plataforma)

        # --- Camara: establecimiento ancho (3/4), apuntando al centro ---
        self.set_camera_orientation(
            phi=60 * DEGREES, theta=-50 * DEGREES, frame_center=[0, 0, 1.2]
        )

        # --- Footprints: nacen todos juntos ---
        self.play(
            FadeIn(VGroup(*[footprint(t) for t in TOWERS]), scale=0.5),
            run_time=0.8,
        )

        # --- La ciudad se construye: fila de atras -> fila del frente ---
        # Orden visual: back (y=1.5), middle (y=0), front (y=-1.5)
        columnas = {}
        orden = sorted(TOWERS, key=lambda t: -t[3])
        for t in orden:
            x, y = t[2], t[3]
            col = torre(t)
            flat = col.copy()
            # OJO: Prism es alto en Z (depth). stretch_to_fit_height encoge Y
            # (torre finita de costado = materializa de cualquier lado).
            flat.stretch_to_fit_depth(0.04)
            flat.move_to([x, y, Z_PISO + 0.02])

            self.add_sound(BLIP_COL)
            self.play(
                Transform(flat, col),
                run_time=0.4,
                rate_func=ease_out_expo,
            )
            columnas[(x, y)] = flat
        self.wait(0.5)

        # --- Orbita suave + la camara baja un poco (sentir la profundidad) ---
        self.move_camera(
            phi=54 * DEGREES,
            theta=-25 * DEGREES,
            frame_center=[0, 0, 1.2],
            run_time=3.0,
            rate_func=smooth,
        )
        self.begin_ambient_camera_rotation(rate=0.03)

        # --- UI de marca (fija en pantalla, nunca rota con la camara) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=TERRACOTA, stroke_width=0).move_to(
                [-5.9, 3.05, 0]
            ),
            Rectangle(width=3.6, height=0.02, fill_color=TINTA, stroke_width=0).next_to(
                [-5.9 + 0.9 / 2, 3.05, 0], RIGHT, buff=0.0
            ),
        )

        label = Text(
            "ALTURA DE RASCACIELOS · EN METROS",
            font=FONT_MONO,
            font_size=22,
            color=TINTA,
        ).to_corner(UL, buff=0.6)

        titulo = Text(
            "Las 12 torres más altas del mundo",
            font=FONT_TITULO,
            font_size=40,
            weight=BOLD,
            color=TINTA,
        ).to_corner(UL, buff=1.3)

        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=TINTA)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=TERRACOTA, stroke_width=0)
        wordmark_c = Text(
            "en Criollo",
            font=FONT_DISPLAY,
            font_size=25,
            slant=ITALIC,
            color=TINTA,
        )
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.scale(0.85).to_corner(DL, buff=0.55)

        self.add_fixed_in_frame_mobjects(filete, label, titulo, wordmark)
        self.play(
            FadeIn(filete), FadeIn(label), FadeIn(titulo), FadeIn(wordmark),
            run_time=1.2,
        )

        # --- Vuelo 1: la camara sube y se hunde sobre la ciudad (dive) ---
        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=80 * DEGREES,
            theta=-55 * DEGREES,
            zoom=1.08,
            frame_center=[0, 0, 3.0],
            run_time=2.2,
            rate_func=ease_in_out_cubic,
        )

        # --- Vuelo 2: sweep lateral sobre los techos (drone sobre la ciudad) ---
        self.move_camera(
            phi=74 * DEGREES,
            theta=-75 * DEGREES,
            zoom=1.0,
            frame_center=[3.6, -1.8, 2.4],
            run_time=3.5,
            rate_func=smooth,
        )

        # --- La torre heroica: nos acercamos ---
        hero = next(t for t in TOWERS if t[1] == 828)
        hx, hy = hero[2], hero[3]
        self.move_camera(
            phi=58 * DEGREES,
            theta=-50 * DEGREES,
            zoom=0.95,
            frame_center=[hx, hy, 3.5],
            run_time=2.0,
            rate_func=smooth,
        )

        # Highlight sin intersecciones: iluminacion + la torre sale adelante.
        hero_col = columnas[(hx, hy)]
        self.add_sound(BLIP_PROTA)
        self.play(
            hero_col.animate.set_fill(
                ManimColor(TERRACOTA).interpolate(ManimColor(WHITE), 0.55)
            ),
            run_time=0.5,
            rate_func=smooth,
        )
        self.play(
            hero_col.animate.set_fill(TERRACOTA),
            run_time=0.5,
            rate_func=smooth,
        )
        # Semantica: adelante = importante (pop hacia la camara)
        self.play(
            hero_col.animate.shift(0.55 * OUT),
            run_time=1.0,
            rate_func=ease_out_expo,
        )

        # Anotacion heroica (2D, fixed-in-frame)
        banner = VGroup(
            Rectangle(width=7.6, height=1.5, fill_color=PAPEL2, stroke_color=TINTA, stroke_width=3),
            Text(
                HERO_NOMBRE,
                font=FONT_TITULO,
                font_size=34,
                weight=BOLD,
                color=TINTA,
            ).move_to([0, 0.32, 0]),
            Text(
                HERO_DATO,
                font=FONT_CUERPO,
                font_size=24,
                color=TINTA_MED,
            ).move_to([0, -0.28, 0]),
        )
        banner.to_corner(DL, buff=0.9).shift(RIGHT * 0.6)
        self.add_fixed_in_frame_mobjects(banner)
        self.add_sound(BLIP_COL)
        self.play(FadeIn(banner, shift=UP * 0.3), run_time=0.7, rate_func=ease_out_expo)
        self.wait(1.3)
        self.play(FadeOut(banner), run_time=0.5)

        # --- Money shot: la camara sube y revela el skyline completo desde arriba ---
        self.add_sound(BLIP_CIERRE)
        self.move_camera(
            phi=86 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.8,
            frame_center=[0, 0, 1.0],
            run_time=3.0,
            rate_func=ease_in_out_cubic,
        )
        self.begin_ambient_camera_rotation(rate=0.02)

        # Cierre: ghost number + subtexto
        ghost = Text(
            "828",
            font=FONT_DISPLAY,
            font_size=240,
            weight=BOLD,
            color=TINTA,
            fill_opacity=GHOST_OPACITY,
        ).to_corner(DR, buff=-0.15)
        cierre = Text(
            "La torre más alta del mundo",
            font=FONT_CUERPO,
            font_size=28,
            color=TINTA_MED,
        ).to_corner(DL, buff=0.9)
        self.add_fixed_in_frame_mobjects(ghost, cierre)
        self.play(FadeIn(ghost), FadeIn(cierre), run_time=0.9)
        self.wait(1.8)
