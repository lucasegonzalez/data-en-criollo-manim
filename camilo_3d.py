"""Demo 3D — Caso Camilo · Bogota (Data en Criollo).

Historia real del vault: Camilo abre su restaurante, los findes se llenan pero
el margen no cierra. El dato (margen por dia) revela que MARTES-MIERCOLES-JUEVES
hacen 2/3 del margen. Pareto aplicado al menu: +34% en 90 dias.

Look: diorama de papel 3D con la marca (Print Nostalgia).
- Columnas nacen de footprints en la plataforma
- Camara centrada en el diorama, orbita suave
- Highlight SIN intersecciones (iluminacion + desplazamiento) para evitar z-fighting
- Sonido sincronizado en vivo + fondo paper grain

Run (mp4 con audio):
  ~/miniforge3/envs/manim/bin/manim render -q m camilo_3d.py CamiloPareto3D
"""

import os

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_expo
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_COL = os.path.join(BASE, "assets/blip_col.wav")
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

DIA_NOMBRES = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]
DIA_ALTURAS = [3.0, 8.5, 9.5, 7.5, 4.0, 5.0, 5.5]  # margen relativo por dia
DIA_COLORES = [STEEL, TERRACOTA, MOSTAZA, BURDEOS, TINTA_MED, OLIVA, STEEL]
SPACING = 1.3
X_DIAS = [i * SPACING for i in range(7)]  # 0 .. 7.8
CENTRO = 3.9  # centro del diorama en x

# Las 3 columnas protagonistas (indices): martes, miercoles, jueves
PROTA = [1, 2, 3]
Z_PISO = 0.03  # altura del nacimiento sobre la plataforma


def footprint(i: int) -> Prism:
    """Casillero en la plataforma del que nace la columna i."""
    f = Prism(
        dimensions=(0.64, 0.64, 0.03),
        fill_color=PAPEL2,
        fill_opacity=1,
        stroke_color=DIA_COLORES[i],
        stroke_width=3,
    )
    f.move_to([X_DIAS[i], 0, Z_PISO / 2])
    return f


def columna_dia(i: int) -> Prism:
    """Prism 3D para el dia i, con el bottom apoyado en Z_PISO."""
    h = DIA_ALTURAS[i]
    col = Prism(
        dimensions=(0.62, 0.62, h),
        fill_color=DIA_COLORES[i],
        fill_opacity=0.95,
        stroke_color=TINTA,
        stroke_width=4,
    )
    col.move_to([X_DIAS[i], 0, Z_PISO + h / 2])
    return col


class CamiloPareto3D(ThreeDScene):
    def construct(self):
        # --- Fondo texturado (paper grain) + plataforma ---
        self.camera.background_color = PAPEL
        fondo = ImageMobject(os.path.join(BASE, "assets/papel_grain.png"))
        fondo.scale(2.4).move_to([CENTRO, 0, -30])
        self.add(fondo)

        plataforma = Prism(
            dimensions=(10.2, 8.2, 0.12),
            fill_color=PAPEL2,
            fill_opacity=1,
            stroke_color=TINTA,
            stroke_width=2,
        )
        plataforma.move_to([CENTRO, 0, -0.06])
        self.add(plataforma)

        # --- Columnas por dia ---
        columnas = [columna_dia(i) for i in range(7)]

        # Etiquetas de dias sobre la plataforma
        etiquetas = VGroup()
        for i in range(7):
            t = Text(
                DIA_NOMBRES[i],
                font=FONT_MONO,
                font_size=24,
                color=TINTA,
            )
            t.move_to([X_DIAS[i], -1.7, Z_PISO + 0.12])
            etiquetas.add(t)

        # --- Camara: centrada en el diorama, vista frontal con angulo ---
        self.set_camera_orientation(
            phi=62 * DEGREES, theta=-55 * DEGREES, frame_center=[CENTRO, 0, 1.5]
        )

        # --- Animacion 1: columnas NACEN de los footprints ---
        for i, lab in zip(range(7), etiquetas):
            foot = footprint(i)
            self.play(FadeIn(foot, scale=0.4), run_time=0.2)

            col = columnas[i]
            flat = col.copy()
            flat.stretch_to_fit_height(0.04)
            flat.move_to([X_DIAS[i], 0, Z_PISO + 0.02])

            self.add_sound(BLIP_COL)  # blip en este momento exacto
            self.play(
                Transform(flat, col),
                FadeIn(lab, shift=UP * 0.2),
                run_time=1.0,
                rate_func=ease_out_expo,  # "pop" final, estilo barra Vox
            )
            columnas[i] = flat
        self.wait(0.6)

        # --- Animacion 2: orbita SUAVE de la camara (subtle, no gira el mundo) ---
        self.move_camera(
            phi=58 * DEGREES,
            theta=-30 * DEGREES,
            frame_center=[CENTRO, 0, 1.5],
            run_time=3.5,
            rate_func=smooth,
        )
        self.begin_ambient_camera_rotation(rate=0.04)

        # --- UI de marca (fija en pantalla, nunca rota con la camara) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=TERRACOTA, stroke_width=0).move_to(
                [-5.6, 3.05, 0]
            ),
            Rectangle(width=3.6, height=0.02, fill_color=TINTA, stroke_width=0).next_to(
                [-5.6 + 0.9 / 2, 3.05, 0], RIGHT, buff=0.0
            ),
        )

        label = Text(
            "MARGEN POR DIA · CAMILO, BOGOTA",
            font=FONT_MONO,
            font_size=24,
            color=TINTA,
        ).to_corner(UL, buff=0.6)

        titulo = Text(
            "TRES DIAS HACEN DOS TERCIOS DEL MARGEN",
            font=FONT_TITULO,
            font_size=40,
            weight=BOLD,
            color=TINTA,
        ).to_corner(UL, buff=1.35)

        dato = Text(
            "67% del margen viene de MAR-MIE-JUE",
            font=FONT_CUERPO,
            font_size=26,
            color=TINTA_MED,
        ).next_to(titulo, DOWN, buff=0.35)

        ghost = Text(
            "67",
            font=FONT_DISPLAY,
            font_size=240,
            weight=BOLD,
            color=TINTA,
            fill_opacity=GHOST_OPACITY,
        ).to_corner(DR, buff=-0.15)

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

        self.add_fixed_in_frame_mobjects(
            filete, label, titulo, dato, ghost, wordmark
        )
        self.play(
            FadeIn(filete), FadeIn(label), FadeIn(titulo),
            FadeIn(dato), FadeIn(ghost), FadeIn(wordmark),
            run_time=1.2,
        )

        # --- Animacion 3: highlight del grupo protagonista ---
        # Sin intersecciones: iluminacion secuencial + el grupo sale adelante.
        for idx in PROTA:
            col = columnas[idx]
            base_color = DIA_COLORES[idx]
            self.add_sound(BLIP_PROTA)
            self.play(
                col.animate.set_fill(
                    ManimColor(base_color).interpolate(ManimColor(WHITE), 0.55)
                ),
                run_time=0.5,
                rate_func=smooth,
            )
            self.play(
                col.animate.set_fill(base_color),
                run_time=0.5,
                rate_func=smooth,
            )

        # El grupo protagonista se adelanta (shift OUT = hacia la camara)
        # Semantica: adelante = importante (curva de pop, estilo collage)
        self.play(
            *[
                columnas[idx].animate.shift(0.55 * OUT)
                for idx in PROTA
            ],
            run_time=1.2,
            rate_func=ease_out_expo,
        )
        self.wait(1.2)

        # --- Cierre: zoom al dato ---
        self.stop_ambient_camera_rotation()
        self.add_sound(BLIP_CIERRE)
        self.move_camera(
            phi=72 * DEGREES,
            theta=-90 * DEGREES,
            frame_center=[CENTRO, 0, 1.5],
            zoom=1.1,
            run_time=2.5,
            rate_func=ease_in_out_cubic,
        )
        self.wait(1.5)
