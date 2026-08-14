"""Fourier 2D — La onda cuadrada como suma de senos (Data en Criollo).

El visual que consagro a Manim (estilo 3Blue1Brown): vectores girando
(epiciclos) y la altura de la punta dibuja una onda. Al sumar armonicos
impares (1, 3, 5, 7) la onda se va volviendo cuadrada.

Diseno limpio: papel sin grano, tipografias de marca, sin 3D, sin
plataforma, sin texto en 3D. Todo 2D puro.

Run (mp4 con audio):
  ~/miniforge3/envs/manim/bin/manim render -q m fourier_onda.py OndaDeFourier
"""

import os

import numpy as np

from manim import *
from manim.utils.rate_functions import linear
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_COL = os.path.join(BASE, "assets/blip_col.wav")
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

CENTRO = np.array([-3.8, 0.0, 0.0])
TRACE_X0 = 0.7          # donde empieza la onda (eje x)
PERIOD_W = 2.6          # ancho de un periodo (2 pi)

# Radio del armonico n (coeficiente de Fourier de la onda cuadrada), escalado
def r(n):
    return (4.0 / (np.pi * n)) * 0.72

CICLOS = [
    # (armonicos, color de la traza, label)
    ([1], STEEL, "UN VECTOR GIRA · LA ALTURA DIBUJA UNA ONDA"),
    ([1, 3], MOSTAZA, "SE SUMA EL ARMONICO 3 · MAS CUADRADA"),
    ([1, 3, 5], OLIVA, "SE SUMA EL ARMONICO 5 · TODAVIA MAS"),
    ([1, 3, 5, 7], TERRACOTA, "SE SUMA EL ARMONICO 7 · CASI CUADRADA"),
]


class OndaDeFourier(Scene):
    def construct(self):
        self.camera.background_color = PAPEL
        theta = ValueTracker(0)
        ACTIVOS = []

        # --- Posiciones de los epiciclos ---
        def joint(n):
            x = sum(r(k) * np.cos(k * theta.get_value()) for k in ACTIVOS if k <= n)
            y = sum(r(k) * np.sin(k * theta.get_value()) for k in ACTIVOS if k <= n)
            return CENTRO + np.array([x, y, 0.0])

        def tip_pos():
            x = sum(r(k) * np.cos(k * theta.get_value()) for k in ACTIVOS)
            y = sum(r(k) * np.sin(k * theta.get_value()) for k in ACTIVOS)
            return CENTRO + np.array([x, y, 0.0])

        def pen_pos():
            x = TRACE_X0 + (theta.get_value() % TAU) / TAU * PERIOD_W
            return np.array([x, tip_pos()[1], 0.0])

        def make_harmonic(n):
            circ = always_redraw(
                lambda: Circle(radius=r(n), stroke_color=STEEL, stroke_width=2)
                .set_fill(opacity=0)
                .move_to(joint(n - 1))
            )
            vec = always_redraw(
                lambda: Line(joint(n - 1), joint(n), stroke_color=TINTA, stroke_width=3)
            )
            return circ, vec

        # --- Ejes ---
        eje_h = Line(CENTRO, CENTRO + np.array([TRACE_X0 + PERIOD_W, 0, 0]),
                     color=STEEL, stroke_width=2)
        eje_v = Line(CENTRO + np.array([0, -1.9, 0]), CENTRO + np.array([0, 1.9, 0]),
                     color=STEEL, stroke_width=1).set_opacity(0.5)

        # --- UI de marca (2D, fija) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=TERRACOTA, stroke_width=0).move_to(
                [-5.9, 3.1, 0]
            ),
            Rectangle(width=3.6, height=0.02, fill_color=TINTA, stroke_width=0).next_to(
                [-5.9 + 0.9 / 2, 3.1, 0], RIGHT, buff=0.0
            ),
        )
        label = Text(
            CICLOS[0][2], font=FONT_MONO, font_size=22, color=TINTA,
        ).to_corner(UL, buff=0.65)
        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=TINTA)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=TERRACOTA, stroke_width=0)
        wordmark_c = Text(
            "en Criollo", font=FONT_DISPLAY, font_size=25, slant=ITALIC, color=TINTA,
        )
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.scale(0.85).to_corner(DL, buff=0.55)

        self.play(FadeIn(eje_h), FadeIn(eje_v), run_time=0.6)
        self.play(FadeIn(filete), FadeIn(label), FadeIn(wordmark), run_time=0.6)

        # --- Primer armonico (el circulo madre + su vector) ---
        ACTIVOS.append(1)
        circ1, vec1 = make_harmonic(1)
        self.play(Create(circ1), Create(vec1), run_time=0.8)

        punto = always_redraw(lambda: Dot(point=tip_pos(), radius=0.07, color=TINTA))
        lapiz = always_redraw(lambda: Dot(point=pen_pos(), radius=0.09, color=TINTA))
        proyeccion = always_redraw(
            lambda: DashedLine(tip_pos(), pen_pos(), stroke_color=STEEL, stroke_width=2,
                               dash_length=0.08)
        )
        self.add(punto, lapiz, proyeccion)

        # --- Ciclos: girar y dibujar la onda con cada suma de armonicos ---
        for idx, (armonicos, color_traza, texto) in enumerate(CICLOS):
            if idx > 0:
                n = armonicos[-1]
                ACTIVOS.append(n)
                circ, vec = make_harmonic(n)
                self.add_sound(BLIP_COL)
                self.play(FadeIn(circ), FadeIn(vec), run_time=0.6)
                nuevo_label = Text(texto, font=FONT_MONO, font_size=22, color=TINTA
                                   ).to_corner(UL, buff=0.65)
                self.play(FadeOut(label), FadeIn(nuevo_label), run_time=0.4)
                label = nuevo_label

            trazo = TracedPath(pen_pos, stroke_color=color_traza, stroke_width=6)
            self.add(trazo)
            self.add_sound(BLIP_COL)
            self.play(theta.animate.set_value(TAU), run_time=4.5, rate_func=linear)
            self.wait(0.4)

            if idx < len(CICLOS) - 1:
                self.play(FadeOut(trazo), run_time=0.3)
                theta.set_value(0)

        # --- Cierre: formula + titulo (la traza final queda visible) ---
        # OJO: NO resetear theta aca — la traza final sigue grabando y el salto
        # dibujaria una linea horizontal indeseada.
        self.add_sound(BLIP_PROTA)
        ghost = Text(
            "4/pi", font=FONT_DISPLAY, font_size=220, weight=BOLD, color=TINTA,
            fill_opacity=GHOST_OPACITY,
        ).to_corner(DR, buff=-0.1)
        titulo = Text(
            "Una onda cuadrada es una suma de senos",
            font=FONT_TITULO, font_size=38, weight=BOLD, color=TINTA,
        ).to_corner(UL, buff=1.4)
        formula = Text(
            "onda = 4/pi ( sen x + 1/3 sen 3x + 1/5 sen 5x + 1/7 sen 7x + ... )",
            font=FONT_MONO, font_size=24, color=TINTA_MED,
        ).next_to(titulo, DOWN, buff=0.4)

        self.play(FadeIn(ghost), FadeIn(titulo), FadeIn(formula), run_time=0.9)
        self.add_sound(BLIP_CIERRE)
        self.wait(2.2)
