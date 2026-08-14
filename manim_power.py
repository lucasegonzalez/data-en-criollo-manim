"""Manim Power Demo — "Todo en R es un vector" (Data en Criollo).

Demo DELIBERADO del poder de Manim, no de HTML/CSS:
  - Transform: un "1" se transforma en un vector [1]; 47 cajitas de super se
    contraen en una columna de 47 (morfing de VGroup -> VGroup).
  - ThreeDScene: el data frame tiene PROFUNDIDAD (placas traseras) y rota en 3D
    real mientras la camara hace un swoop a 3/4.
  - move_camera: push-in sutil + camara 3D, todo en la misma pieza.

Concepto CS50R Semana 1 (Representing Data): "TODO en R es un vector".
Un numero es un vector de 1. Una columna es un vector de muchos. Un data frame
es una LISTA DE VECTORES DEL MISMO LARGO.

Reglas de marca (dec_brand.py): modo oscuro, terracota SOLO como senal (filete
de marca + la palabra VECTOR del punchline = misma senal narrativa), sin LaTeX
(todo con Text), tipografias Oswald/Playfair/Cutive.

Run:
  ~/miniforge3/envs/manim/bin/manim render -q l manim_power.py VectorTodo
"""

import os

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, smooth

from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")


def bracket(height, width=0.32, stroke=6, color=DARK_FG, side="left"):
    """Un "[": dos esquinas dibujadas con Lineas (sin LaTeX)."""
    h = height
    if side == "left":
        b = VGroup(
            Line([0, 0, 0], [width, 0, 0], stroke_width=stroke, color=color),
            Line([0, 0, 0], [0, h, 0], stroke_width=stroke, color=color),
            Line([width, h, 0], [0, h, 0], stroke_width=stroke, color=color),
        )
    else:
        b = VGroup(
            Line([0, 0, 0], [0, 0, 0], stroke_width=stroke, color=color),
            Line([width, 0, 0], [width, h, 0], stroke_width=stroke, color=color),
            Line([0, h, 0], [width, h, 0], stroke_width=stroke, color=color),
        )
    return b


def cell(w=1.3, h=0.5, fill=DARK_RAISED, stroke_color=DARK_FG_MED):
    return Rectangle(
        width=w, height=h, fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke_color, stroke_width=1.2, stroke_opacity=0.35,
    )


class VectorTodo(ThreeDScene):
    def construct(self):
        self.camera.background_color = DARK_BG
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # --- UI de marca (fija en frame, no rota con la camara 3D) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=DARK_TERRACOTA, stroke_width=0,
                      ).move_to([-5.9, 3.1, 0]),
            Rectangle(width=3.6, height=0.02, fill_color=DARK_FG, stroke_width=0,
                      ).next_to([-5.9 + 0.45, 3.1, 0], RIGHT, buff=0.0),
        )
        label = Text(
            "CS50R \u00b7 REPRESENTING DATA \u00b7 VECTORES",
            font=FONT_MONO, font_size=22, color=DARK_FG,
        ).to_corner(UL, buff=0.65)
        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=DARK_FG)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=DARK_TERRACOTA, stroke_width=0)
        wordmark_c = Text("en Criollo", font=FONT_DISPLAY, font_size=25, slant=ITALIC, color=DARK_FG)
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.to_corner(DR, buff=0.65)
        self.add_fixed_in_frame_mobjects(filete, label, wordmark)

        # =================================================================
        # ACTO 1 — un numero ES un vector de 1 (Transform + Create)
        # =================================================================
        kicker = Text(
            "UNA COMPRA \u00b7 UN NUMERO",
            font=FONT_MONO, font_size=26, color=STEEL,
        ).to_edge(UP, buff=1.1)
        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(kicker, shift=DOWN * 0.3), run_time=0.8)

        uno = Text("1", font=FONT_DISPLAY, font_size=150, weight=BOLD, color=DARK_FG)
        uno.move_to([-4.3, 0.1, 0])

        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(uno, scale=1.4), run_time=1.1)

        # los corchetes se DIBUJAN alrededor del "1" (Create) -> vector de 1
        br_izq = bracket(1.5).move_to(uno.get_left() + LEFT * 0.45)
        br_der = bracket(1.5, side="right").move_to(uno.get_right() + RIGHT * 0.45)
        vector1 = VGroup(br_izq, uno, br_der)

        self.play(Create(br_izq), Create(br_der), run_time=0.9)
        lab1 = Text(
            "= VECTOR DE 1",
            font=FONT_MONO, font_size=30, color=DARK_MOSTAZA,
        ).next_to(vector1, DOWN, buff=0.6)
        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(lab1, shift=UP * 0.2), run_time=0.7)
        self.wait(0.6)

        # =================================================================
        # ACTO 2 — 47 compras se contraen en una columna (morfing VGroup)
        # =================================================================
        # el vector [1] se corre a la izquierda, queda como "unidad"
        self.play(
            vector1.animate.scale(0.55).to_corner(UL, buff=1.7),
            FadeOut(kicker, shift=UP * 0.2),
            run_time=1.0,
        )

        ticket = Text(
            "EL TICKET DEL SUPER \u00b7 47 COMPRAS",
            font=FONT_MONO, font_size=30, color=DARK_FG,
        ).to_edge(UP, buff=1.1)
        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(ticket, shift=DOWN * 0.3), run_time=0.9)

        # 47 cajitas (una por compra) caen en grilla
        n = 47
        cajas = VGroup(*[
            Square(side_length=0.52, fill_color=DARK_RAISED, fill_opacity=1.0,
                   stroke_color=DARK_FG_MED, stroke_width=1.0, stroke_opacity=0.3)
            for _ in range(n)
        ])
        cajas.arrange_in_grid(rows=6, cols=8, buff=0.09)
        cajas.move_to([0.8, 0, 0])

        self.add_sound(BLIP_PROTA)
        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in cajas],
                        lag_ratio=0.035),
            run_time=2.2,
        )
        self.wait(0.4)

        # morfing: las 47 cajitas vuelan y se apilan en UNA columna
        col_objetivo = VGroup(*[
            Square(side_length=0.52, fill_color=DARK_RAISED, fill_opacity=1.0,
                   stroke_color=DARK_FG_MED, stroke_width=1.0, stroke_opacity=0.3)
            for _ in range(6)
        ])
        col_objetivo.arrange(DOWN, buff=0.09)
        puntos = Text("\u22ee", font=FONT_MONO, font_size=60, color=DARK_FG_MED)
        num47 = Text("47", font=FONT_DISPLAY, font_size=64, weight=BOLD, color=DARK_FG)
        grupo_col = VGroup(col_objetivo[:3], puntos, col_objetivo[3:])
        grupo_col.arrange(DOWN, buff=0.14)
        grupo_col.move_to([0.8, 0, 0])

        self.add_sound(BLIP_PROTA)
        self.play(
            Transform(cajas, grupo_col),
            run_time=2.4,
            rate_func=ease_in_out_cubic,
        )

        # corchetes de la columna + etiqueta
        alto_col = grupo_col.height
        b_izq = bracket(alto_col).move_to(grupo_col.get_left() + LEFT * 0.4)
        b_der = bracket(alto_col, side="right").move_to(grupo_col.get_right() + RIGHT * 0.4)
        col_final = VGroup(b_izq, cajas, b_der)

        self.play(Create(b_izq), Create(b_der), run_time=0.7)
        lab2 = Text(
            "= VECTOR DE 47",
            font=FONT_MONO, font_size=30, color=DARK_MOSTAZA,
        ).next_to(col_final, DOWN, buff=0.6)
        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(lab2, shift=UP * 0.2), run_time=0.7)
        self.wait(0.6)

        # =================================================================
        # ACTO 3 — el data frame en 3D (ThreeDScene + camara real)
        # =================================================================
        # limpiar acto 2 hacia la derecha; entra la tabla
        self.play(
            FadeOut(ticket, shift=UP * 0.2),
            FadeOut(lab2, shift=DOWN * 0.2),
            col_final.animate.scale(0.5).to_corner(UR, buff=1.7),
            run_time=1.0,
        )

        titulo_tabla = Text(
            "DATA FRAME \u00b7 LISTA DE VECTORES DEL MISMO LARGO",
            font=FONT_MONO, font_size=26, color=DARK_FG,
        ).to_edge(UP, buff=1.1)
        self.add_sound(BLIP_PROTA)
        self.play(FadeIn(titulo_tabla, shift=DOWN * 0.3), run_time=0.9)

        # 3 columnas con placa trasera (profundidad real para el 3D)
        cols = []
        for cx in [-2.4, 0.0, 2.4]:
            col = VGroup(*[cell() for _ in range(6)])
            col.arrange(DOWN, buff=0.08)
            col.move_to([cx, 0, 0])
            # placa trasera: copia offset en Z, mas oscura -> profundidad
            back = col.copy().shift(OUT * 0.4).set_fill(TINTA_MED, opacity=0.55)
            back.set_stroke(opacity=0.0)
            cols.append(VGroup(back, col))
        header = Text("ITEM \u00b7 CANTIDAD \u00b7 PRECIO",
                      font=FONT_MONO, font_size=26, color=DARK_FG_MED)
        header.move_to([0, 2.4, 0])

        tabla = VGroup(*cols, header)
        self.play(FadeIn(header, shift=DOWN * 0.2), run_time=0.6)
        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in cols], lag_ratio=0.25),
            run_time=1.8,
        )
        self.wait(0.3)

        # CAMARA: swoop a 3/4 para revelar la profundidad
        self.move_camera(phi=52 * DEGREES, theta=-38 * DEGREES,
                         run_time=2.2, rate_func=smooth)

        # el data frame rota en 3D real
        self.play(
            Rotate(tabla, angle=38 * DEGREES, axis=UP, run_time=2.4,
                   rate_func=ease_in_out_cubic),
        )
        self.wait(0.5)

        # cada columna se ILUMINA ENTERA (halo + "$" + nombre) -> el dolar de R
        nombres = ["$ITEM", "$CANTIDAD", "$PRECIO"]
        for i, (grp, nombre) in enumerate(zip(cols, nombres)):
            col_visible = grp[1]
            halo = Rectangle(
                width=col_visible.width + 0.5, height=col_visible.height + 0.4,
                fill_color=DARK_MOSTAZA, fill_opacity=0.16,
                stroke_color=DARK_MOSTAZA, stroke_width=2, stroke_opacity=0.7,
            ).move_to(col_visible)
            etiqueta = Text(nombre, font=FONT_MONO, font_size=30, color=DARK_MOSTAZA)
            etiqueta.move_to([col_visible.get_center()[0], 0, 0.6])
            self.add_sound(BLIP_PROTA)
            self.play(
                FadeIn(halo, scale=1.15),
                FadeIn(etiqueta, shift=UP * 0.25),
                run_time=0.6,
            )
            self.wait(0.25)

        self.wait(0.5)

        # =================================================================
        # CIERRE — punchline (fija en frame, camara a plano)
        # =================================================================
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES,
                         run_time=1.6, rate_func=smooth)

        punch = VGroup(
            Text("TODO", font=FONT_DISPLAY, font_size=64, weight=BOLD, color=DARK_FG),
            Text("EN R ES UN", font=FONT_DISPLAY, font_size=64, weight=BOLD, color=DARK_FG),
            Text("VECTOR", font=FONT_DISPLAY, font_size=64, weight=BOLD, color=DARK_TERRACOTA),
        )
        punch.arrange(RIGHT, buff=0.35)
        punch.move_to([0, -0.5, 0])
        self.add_fixed_in_frame_mobjects(punch)

        self.add_sound(BLIP_CIERRE)
        self.play(
            FadeIn(punch, scale=0.8, shift=UP * 0.4),
            run_time=1.2,
        )
        self.wait(1.6)
        self.play(FadeOut(punch, scale=0.9), run_time=0.8)
