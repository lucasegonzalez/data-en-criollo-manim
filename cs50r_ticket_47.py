"""Pieza 1 · CS50R — El ticket de las 47 compras (Data en Criollo).

Cold open real del guion PS1: un tipo en Buenos Aires compro 47 cosas online
(MercadoLibre, Amazon, el super del barrio) y no supo cuanto gasto hasta que
llego la tarjeta — "ese tipo soy yo". La tesis de la Semana 1:

    TODO EN R ES UN VECTOR.

Un numero es un vector de 1; una columna es un vector de muchos; un data frame
es una LISTA DE VECTORES DEL MISMO LARGO. Excel piensa en celdas; R opera
sobre el vector completo, sin loops.

Secuencia (arco narrativo):
  1. El ticket: super arrugado, crema, tinta, montos en Cutive Mono, ghost "47".
  2. Se desarma en 47 cajitas (pops con ease_out_expo, rafagas de sonido al
     inicio y al final del desarme, sin ametralladora).
  3. Una cajita se separa -> "VECTOR DE 1". Punchline: "47 cosas. Una sola
     cosa para R."
  4. Las 47 se alinean en grilla, un arco OLIVA las envuelve -> sum(vector)
     en una pasada. Total revelado en TERRACOTA (unica vez de la pieza).
  5. El ticket es un data frame: cabecera item · cantidad · precio; cada
     columna se ilumina ENTERA con "$" + nombre (operador $ de R).
  6. Cierre: "Saber leer un CSV es un superpoder" + stat de la serie.

Look: papel Print Nostalgia, misma UI de marca que camilo_3d.py (filete,
label, titulo Oswald sentence case, ghost number, wordmark), fondo con grano,
camara 2D con movimientos SUBTILES (zoom-in al sumar, zoom-out al cierre).

Run (mp4 con audio):
  ~/miniforge3/envs/manim/bin/manim render -q m cs50r_ticket_47.py ElTicketDeLas47Compras
"""

import os
import random

import numpy as np
from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_expo
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_COL = os.path.join(BASE, "assets/blip_col.wav")
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")
BLIP_POP = os.path.join(BASE, "assets/blip_pop.wav")
BLIP_BURST = os.path.join(BASE, "assets/blip_burst.wav")
BLIP_SUM = os.path.join(BASE, "assets/blip_sum.wav")

N_ITEMS = 47
TOTAL = "187.400"
HERO_SCALE = 1.9

# Items visibles del ticket (12 de 47): el resto queda en "... 35 ITEMS MAS".
# Subtotal visible: 181.700 -> faltan 5.700 para el total de 187.400.
ITEMS = [
    ("PAN", "1.200"),
    ("LECHE", "2.800"),
    ("EMPANADAS (12)", "9.600"),
    ("YERBA", "5.200"),
    ("GALLETITAS", "3.400"),
    ("ARROZ", "2.900"),
    ("QUESO", "7.800"),
    ("TOMATES", "1.100"),
    ("CABLE HDMI", "11.500"),
    ("AURICULARES", "42.900"),
    ("ZAPATILLAS", "68.000"),
    ("MOCHILA", "25.300"),
]

# Paleta de cajitas: papel dominante, acentos de marca muy diluidos.
CAJA_PLAIN = (PAPEL2, 1.0)
CAJA_TINTS = [
    (CREMA, 1.0),
    (STEEL, 0.35),
    (OLIVA, 0.28),
    (MOSTAZA, 0.32),
    (CREMA, 1.0),
]
CAJA_HERO = (MOSTAZA, 0.45)


def tracked(text: str) -> str:
    """Tracking amplio para labels Cutive Mono (manim 0.20 no tiene `tracking`)."""
    return " ".join(text)


def tracked_words(text: str) -> str:
    """Tracking amplio suave entre palabras (para la stat larga)."""
    return text.replace(" ", "  ")


def linea_ticket(nombre: str, monto: str, ancho: int = 26) -> Text:
    """Linea del ticket: nombre + guia de puntos + monto (Cutive Mono)."""
    relleno = "." * max(2, ancho - len(nombre) - len(monto))
    return Text(
        f"{nombre} {relleno} {monto}",
        font=FONT_MONO,
        font_size=22,
        color=TINTA,
    )


def build_receipt() -> VGroup:
    """El ticket de super: crema, arrugado (rotacion + pliegue), total abajo."""
    header1 = Text(
        "SUPERMERCADO DEL BARRIO",
        font=FONT_MONO,
        font_size=26,
        color=TINTA,
    )
    header2 = Text(
        "compras online · mercado libre · amazon",
        font=FONT_CUERPO,
        font_size=20,
        slant=ITALIC,
        color=TINTA_MED,
    )
    div = Text("-" * 30, font=FONT_MONO, font_size=20, color=TINTA_MED)
    lineas = [linea_ticket(nombre, monto) for nombre, monto in ITEMS]
    resto = Text(
        ". . . 35 ITEMS MAS . . .",
        font=FONT_MONO,
        font_size=20,
        color=TINTA_MED,
    )
    total = linea_ticket("TOTAL · 47 ITEMS", f"${TOTAL}", ancho=24)
    total.scale(1.25).set_color(TINTA)

    cuerpo = VGroup(
        header1, header2, div, *lineas, resto, div.copy(), total
    ).arrange(DOWN, buff=0.09)
    cuerpo.scale_to_fit_width(5.9)

    sombra = Rectangle(
        width=cuerpo.width + 0.22,
        height=cuerpo.height + 0.22,
        fill_color=STEEL,
        fill_opacity=0.14,
        stroke_width=0,
    ).shift(DOWN * 0.09 + RIGHT * 0.09)

    papel = Rectangle(
        width=cuerpo.width + 0.34,
        height=cuerpo.height + 0.34,
        fill_color=CREMA,
        fill_opacity=1,
        stroke_color=TINTA,
        stroke_width=2.5,
    )

    pliegue = Line(
        UP * (cuerpo.height / 2 + 0.30),
        DOWN * (cuerpo.height / 2 + 0.30),
        color=TINTA,
        stroke_width=1,
    ).set_stroke(opacity=0.10)

    ticket = VGroup(sombra, papel, pliegue, cuerpo).rotate(-2.5 * DEGREES)
    return ticket


def build_cajas() -> list:
    """47 cajitas (1 por item): posiciones en nube (disco) + colores de papel."""
    rng = random.Random(47)
    cajas = []
    for i in range(N_ITEMS):
        r = rng.random() ** 0.5
        ang = rng.uniform(0, 2 * np.pi)
        x = r * 2.25 * np.cos(ang)
        y = r * 1.45 * np.sin(ang)
        if i == 0:
            color, opacidad = CAJA_HERO
        elif i % 5 == 0:
            color, opacidad = CAJA_TINTS[(i // 5) % len(CAJA_TINTS)]
        else:
            color, opacidad = CAJA_PLAIN
        caja = Square(
            side_length=0.42,
            fill_color=color,
            fill_opacity=opacidad,
            stroke_color=TINTA,
            stroke_width=2.5,
        ).move_to([x, y, 0])
        cajas.append(caja)
    return cajas


def build_ui() -> VGroup:
    """UI de marca fija (misma estructura que camilo_3d.py; en 2D todo es fijo).

    El filete va en TINTA/STEEL (no terracota): la unica aparicion de
    TERRACOTA en la pieza es el total revelado en el beat 4.
    """
    filete = VGroup(
        Rectangle(width=0.9, height=0.06, fill_color=TINTA, stroke_width=0).move_to(
            [-5.6, 3.05, 0]
        ),
        Rectangle(width=3.6, height=0.02, fill_color=STEEL, stroke_width=0).next_to(
            [-5.6 + 0.9 / 2, 3.05, 0], RIGHT, buff=0.0
        ),
    )
    label = Text(
        "CS50R · SEMANA 1 · TODO ES UN VECTOR",
        font=FONT_MONO,
        font_size=24,
        color=TINTA,
    ).to_corner(UL, buff=0.6)
    titulo = Text(
        "Todo es un vector",
        font=FONT_TITULO,
        font_size=40,
        weight=BOLD,
        color=TINTA,
    ).to_corner(UL, buff=1.35)
    ghost = Text(
        "47",
        font=FONT_DISPLAY,
        font_size=240,
        weight=BOLD,
        color=TINTA,
        fill_opacity=GHOST_OPACITY,
    ).to_corner(DR, buff=-0.15)
    wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=TINTA)
    divisor = Rectangle(width=0.045, height=0.55, fill_color=MOSTAZA, stroke_width=0)
    wordmark_c = Text(
        "en Criollo",
        font=FONT_DISPLAY,
        font_size=25,
        slant=ITALIC,
        color=TINTA,
    )
    wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
    wordmark.scale(0.85).to_corner(DL, buff=0.55)
    return VGroup(filete, label, titulo, ghost, wordmark)


class ElTicketDeLas47Compras(MovingCameraScene):
    def construct(self):
        # ------------------------------------------------------------ fondo
        self.camera.background_color = PAPEL
        fondo = ImageMobject(os.path.join(BASE, "assets/papel_grain.png"))
        fondo.scale(2.4).move_to(ORIGIN)
        self.add(fondo)

        # ------------------------------------------------------- beat 1: el ticket
        ticket = build_receipt()
        self.add_sound(BLIP_COL)
        self.play(
            FadeIn(ticket, scale=0.85, shift=DOWN * 0.25),
            run_time=1.4,
            rate_func=ease_out_expo,
        )
        self.wait(2.0)

        ui = build_ui()
        self.play(FadeIn(ui), run_time=1.2)
        self.wait(0.8)
        self.wait(9.0)  # tiempo de lectura del ticket

        # ------------------------------------------------------- beat 2: se desarma
        self.play(FadeOut(ticket), run_time=0.5)
        cajas = build_cajas()
        primera_mitad = cajas[:24]
        segunda_mitad = cajas[24:]

        self.add_sound(BLIP_BURST)
        self.play(
            LaggedStart(
                *[
                    FadeIn(c, scale=0.3, rate_func=ease_out_expo)
                    for c in primera_mitad
                ],
                lag_ratio=0.05,
                run_time=0.4,
            )
        )
        self.wait(0.4)
        self.add_sound(BLIP_BURST)
        self.play(
            LaggedStart(
                *[
                    FadeIn(c, scale=0.3, rate_func=ease_out_expo)
                    for c in segunda_mitad
                ],
                lag_ratio=0.05,
                run_time=0.4,
            )
        )
        self.wait(5.0)  # la nube de 47 cajitas

        # ----------------------------------- beat 3: una cajita se separa
        heroe = cajas[0]
        self.add_sound(BLIP_POP)
        self.play(
            heroe.animate.scale(HERO_SCALE),
            run_time=0.6,
            rate_func=ease_out_expo,
        )
        self.play(
            heroe.animate.move_to([0.0, 1.95, 0]),
            run_time=0.7,
            rate_func=ease_out_expo,
        )
        etiqueta_vector = Text(
            tracked("VECTOR DE 1"),
            font=FONT_MONO,
            font_size=24,
            color=TINTA,
        ).next_to(heroe, RIGHT, buff=0.45).scale_to_fit_width(4.8)
        self.add_sound(BLIP_COL)
        self.play(FadeIn(etiqueta_vector, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(0.6)

        punchline_3 = Text(
            "47 cosas. Una sola cosa para R.",
            font=FONT_CUERPO,
            font_size=30,
            slant=ITALIC,
            color=TINTA_MED,
        ).move_to([0, -2.75, 0])
        self.play(FadeIn(punchline_3, shift=UP * 0.2), run_time=0.8)
        self.wait(5.5)

        # --------------------------------------- beat 4: alineacion + sum(vector)
        self.play(FadeOut(punchline_3), run_time=0.4)
        self.play(FadeOut(etiqueta_vector), run_time=0.4)
        self.play(
            heroe.animate.scale(1 / HERO_SCALE).set_fill(PAPEL2, opacity=1.0),
            run_time=0.5,
            rate_func=ease_out_expo,
        )

        # grilla 8x6 (47 cajitas + 1 casillero vacio)
        plantilla = VGroup(*[Square(side_length=0.42) for _ in range(48)])
        plantilla.arrange_in_grid(rows=6, cols=8, buff=0.14)
        grilla = [s.get_center() for s in plantilla]

        anims = [caja.animate.move_to(grilla[i]) for i, caja in enumerate(cajas)]

        self.add_sound(BLIP_PROTA)
        self.play(
            *anims,
            self.camera.frame.animate.scale(0.94).move_to([0, 0, 0]),
            run_time=2.2,
            rate_func=ease_out_expo,
        )
        self.wait(0.5)

        grupo = VGroup(*cajas)
        arco = Brace(grupo, direction=DOWN, buff=0.10).set_color(OLIVA)
        sum_txt = Text(
            "sum(vector)",
            font=FONT_MONO,
            font_size=32,
            color=OLIVA,
        ).next_to(arco, DOWN, buff=0.12)
        self.add_sound(BLIP_SUM)
        self.play(
            FadeIn(arco, scale=0.6),
            FadeIn(sum_txt, shift=DOWN * 0.2),
            run_time=1.0,
            rate_func=ease_out_expo,
        )

        total_txt = Text(
            f"= ${TOTAL}",
            font=FONT_MONO,
            font_size=46,
            color=TERRACOTA,
        ).next_to(sum_txt, DOWN, buff=0.18)
        self.add_sound(BLIP_POP)
        self.play(
            FadeIn(total_txt, scale=0.6),
            run_time=0.8,
            rate_func=ease_out_expo,
        )
        self.wait(6.5)  # el numero que el tipo no sabia

        # ------------------------------- beat 5: el ticket es un data frame
        self.play(
            FadeOut(arco), FadeOut(sum_txt), FadeOut(total_txt), run_time=0.5
        )

        cabecera = Text(
            tracked_words("ITEM · CANTIDAD · PRECIO"),
            font=FONT_MONO,
            font_size=26,
            color=TINTA,
        ).move_to([0, 2.35, 0])
        self.add_sound(BLIP_COL)
        self.play(FadeIn(cabecera, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.8)

        # tres bandas verticales = las tres columnas del data frame
        nombres = ["$item", "$cantidad", "$precio"]
        bandas = [[], [], []]
        for caja in cajas:
            x = caja.get_center()[0]
            if x < -0.72:
                bandas[0].append(caja)
            elif x < 0.72:
                bandas[1].append(caja)
            else:
                bandas[2].append(caja)
        etiquetas_dolar = []
        for k, (nombre, banda) in enumerate(zip(nombres, bandas)):
            x = -1.44 + k * 1.44
            self.add_sound(BLIP_POP)
            self.play(
                *[b.animate.set_fill(CREMA, opacity=1.0) for b in banda],
                run_time=0.6,
            )
            etq = Text(
                nombre,
                font=FONT_MONO,
                font_size=28,
                color=OLIVA,
            ).move_to([x, 1.95, 0])
            etiquetas_dolar.append(etq)
            self.play(FadeIn(etq, shift=UP * 0.15), run_time=0.35)
            self.wait(0.3)

        punchline_5 = Text(
            "De la tabla, traeme la columna.",
            font=FONT_CUERPO,
            font_size=30,
            slant=ITALIC,
            color=TINTA_MED,
        ).move_to([0, -2.6, 0])
        self.play(FadeIn(punchline_5, shift=UP * 0.2), run_time=0.8)
        self.wait(5.5)

        # ----------------------------------------------- beat 6: cierre
        salir = VGroup(grupo, cabecera, *etiquetas_dolar, punchline_5)
        self.play(FadeOut(salir), run_time=0.8)
        self.play(
            self.camera.frame.animate.scale(1.0).move_to([0, 0.2, 0]),
            run_time=1.2,
            rate_func=ease_in_out_cubic,
        )

        titulo_cierre = Text(
            "Saber leer un CSV es un superpoder",
            font=FONT_TITULO,
            font_size=44,
            weight=BOLD,
            color=TINTA,
        ).move_to([0, 0.9, 0])
        stat = Text(
            tracked_words("EL 73% DE LAS PYMES EN LATAM NO USA SUS PROPIOS DATOS"),
            font=FONT_MONO,
            font_size=28,
            color=BURDEOS,
        ).scale_to_fit_width(10.5).move_to([0, -0.6, 0])

        self.add_sound(BLIP_CIERRE)
        self.play(
            FadeIn(titulo_cierre, scale=0.9),
            FadeIn(stat, scale=0.9, shift=UP * 0.15),
            run_time=1.4,
            rate_func=ease_out_expo,
        )
        self.wait(7.0)
