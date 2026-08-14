"""EOQ Supply Chain 2D — Cantidad Economica de Pedido (Data en Criollo).

Estilo 3Blue1Brown aplicado a supply chain: aparece la formula, se remarca
elemento por elemento (cada variable con su color semantico) y despues se
DIBUJAN las curvas de costo. El punto optimo (EOQ) es el resultado POSITIVO
-> oliva (nunca rojo). MODO OSCURO.

Semantica de color (vault Visual/Paleta de Colores.md, variantes oscuras):
- DARK_OLIVA   = positivo / confirmacion  -> Q*, punto optimo + brillo
- DARK_BURDEOS = precio / costo           -> S (costo de ordenar) + curva
- STEEL        = terciario / metadata     -> H (costo de mantener) + curva
- DARK_MOSTAZA = acento 2                 -> D (demanda)
- DARK_FG      = texto (papel sobre tinta)
- DARK_TERRACOTA = acento unico (UNA vez): solo el filete de marca

Datos del ejemplo (Modelos/EOQ.md): D=24.000 cajas/anio, S=$150/pedido,
H=$3/caja/anio  ->  Q* = 1.549 cajas, CT total = $4.649.

Etiquetas de curvas en leyenda a la derecha (fuera del plot) para que
NUNCA se encimen palabras sobre las curvas.

Sonido solo en los momentos clave: remarcado de Q*, punto optimo y cierre.

Run (mp4):
  ~/miniforge3/envs/manim/bin/manim render -q m eoq_supply_chain.py EOQSupplyChain
"""

import os

from manim import *
from manim.utils.rate_functions import ease_out_expo, smooth
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

# Datos del ejemplo
D = 24000.0   # demanda anual (cajas)
S = 150.0     # costo de ordenar por pedido ($)
H = 3.0       # costo de mantener 1 caja 1 anio ($)
Q_STAR = int(round((2 * D * S / H) ** 0.5))  # 1549

# Formula como piezas con color semantico (modo oscuro, sin LaTeX)
FORMULA = [
    ("Q*", DARK_OLIVA), ("=", DARK_FG), ("\u221a(", DARK_FG), ("2", DARK_FG),
    ("\u00b7", DARK_FG), ("D", DARK_MOSTAZA), ("\u00b7", DARK_FG), ("S", DARK_BURDEOS),
    ("/", DARK_FG), ("H", STEEL), (")", DARK_FG),
]

# Chips de explicacion: (swatch_color, texto)
CHIPS = [
    (DARK_MOSTAZA, "D \u00b7 DEMANDA ANUAL \u00b7 24.000 CAJAS"),
    (DARK_BURDEOS, "S \u00b7 COSTO DE ORDENAR \u00b7 $150 POR PEDIDO"),
    (STEEL, "H \u00b7 COSTO DE MANTENER \u00b7 $3 POR CAJA/ANIO"),
    (DARK_OLIVA, "Q* \u00b7 CANTIDAD OPTIMA \u00b7 1.549 CAJAS"),
]


class EOQSupplyChain(Scene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # --- UI de marca (2D, modo oscuro) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=DARK_TERRACOTA, stroke_width=0
                      ).move_to([-5.9, 3.1, 0]),
            Rectangle(width=3.6, height=0.02, fill_color=DARK_FG, stroke_width=0
                      ).next_to([-5.9 + 0.9 / 2, 3.1, 0], RIGHT, buff=0.0),
        )
        label = Text(
            "INVENTARIOS \u00b7 SUPPLY CHAIN \u00b7 EOQ",
            font=FONT_MONO, font_size=22, color=DARK_FG,
        ).to_corner(UL, buff=0.65)
        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=DARK_FG)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=DARK_TERRACOTA, stroke_width=0)
        wordmark_c = Text(
            "en Criollo", font=FONT_DISPLAY, font_size=25, slant=ITALIC, color=DARK_FG,
        )
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.scale(0.85).to_corner(DL, buff=0.55)

        self.play(FadeIn(filete), FadeIn(label), FadeIn(wordmark), run_time=0.6)

        # --- 1) Aparece la formula, pieza por pieza (sin sonido) ---
        formula_pieces = VGroup(*[
            Text(txt, font=FONT_DISPLAY, font_size=46, slant=ITALIC, color=col)
            for txt, col in FORMULA
        ])
        formula_pieces.arrange(RIGHT, buff=0.13).move_to([0, 2.6, 0])

        for p in formula_pieces:
            self.play(FadeIn(p, scale=1.6), run_time=0.3, rate_func=ease_out_expo)
        self.wait(0.4)

        # --- 2) Remarcar cada elemento con su chip de significado ---
        # indices en la formula: D=5, S=7, H=9, Q*=0
        target_idx = [5, 7, 9, 0]

        for idx, (swatch, texto) in zip(target_idx, CHIPS):
            piece = formula_pieces[idx]
            chip = VGroup(
                Rectangle(width=0.16, height=0.16, fill_color=swatch, stroke_width=0),
                Text(texto, font=FONT_MONO, font_size=21, color=DARK_FG),
            ).arrange(RIGHT, buff=0.25)
            chip.next_to(formula_pieces, DOWN, buff=0.45)

            if idx == 0:
                # Q*: momento clave -> brillo oliva detras de la pieza + ping
                self.add_sound(BLIP_PROTA)
                halo = VGroup(
                    Circle(radius=0.42, color=DARK_OLIVA, fill_opacity=0.22, stroke_width=0
                           ).move_to(piece),
                    Circle(radius=0.78, color=DARK_OLIVA, fill_opacity=0.08, stroke_width=0
                           ).move_to(piece),
                )
                self.play(FadeIn(halo, scale=1.4), piece.animate.scale(1.45),
                          run_time=0.45, rate_func=ease_out_expo)
                self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.35)
                self._ping(piece.get_center(), DARK_OLIVA, 2)
                self.wait(0.8)
                self.play(FadeOut(chip), run_time=0.25)
                self.play(FadeOut(halo), piece.animate.scale(1.0 / 1.45), run_time=0.35)
            else:
                self.play(piece.animate.scale(1.45), run_time=0.4, rate_func=ease_out_expo)
                self.play(FadeIn(chip, shift=UP * 0.15), run_time=0.35)
                self.wait(0.55)
                self.play(FadeOut(chip), run_time=0.25)
                self.play(piece.animate.scale(1.0 / 1.45), run_time=0.3)

        # --- 3) Ahora dibujamos: la formula sube para abrir el grafico ---
        self.play(
            formula_pieces.animate.scale(0.62).to_edge(UP, buff=0.3),
            run_time=0.8,
            rate_func=smooth,
        )

        axes = Axes(
            x_range=[0, 6000, 1000],
            y_range=[0, 20000, 5000],
            x_length=5.6,
            y_length=3.2,
            axis_config={"color": DARK_FG, "stroke_width": 2,
                         "include_ticks": False, "include_numbers": False},
        ).move_to([0.4, -1.2, 0])

        xlabel = Text("TAMA\u00d1O DE PEDIDO (Q)", font=FONT_MONO, font_size=18, color=DARK_FG
                      ).next_to(axes, DOWN, buff=0.3)
        ylabel = Text("COSTO ANUAL ($)", font=FONT_MONO, font_size=18, color=DARK_FG
                      ).next_to(axes, LEFT, buff=0.25)

        self.play(Create(axes), FadeIn(xlabel), FadeIn(ylabel), run_time=1.0)

        # --- Leyenda a la derecha (fuera del plot: cero encimadas) ---
        def leyenda_fila(swatch_color, texto):
            return VGroup(
                Rectangle(width=0.14, height=0.14, fill_color=swatch_color, stroke_width=0),
                Text(texto, font=FONT_MONO, font_size=18, color=DARK_FG),
            ).arrange(RIGHT, buff=0.22)

        legend = VGroup(
            leyenda_fila(DARK_BURDEOS, "COSTO DE ORDENAR \u00b7 (D/Q)\u00b7S"),
            leyenda_fila(STEEL, "COSTO DE MANTENER \u00b7 (Q/2)\u00b7H"),
            leyenda_fila(DARK_FG, "COSTO TOTAL"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        legend.next_to(axes, RIGHT, buff=0.55).align_to(axes, UP).shift(DOWN * 0.25)

        # Curva 1: costo de ordenar = (D/Q) * S -> DARK_BURDEOS (decrece)
        ordenar = axes.plot(lambda q: S * D / q, x_range=[250, 6000],
                            color=DARK_BURDEOS, stroke_width=5)
        self.play(Create(ordenar), FadeIn(legend[0]), run_time=1.4, rate_func=smooth)

        # Curva 2: costo de mantener = (Q/2) * H -> STEEL (crece)
        mantener = axes.plot(lambda q: H * q / 2, x_range=[0, 6000],
                             color=STEEL, stroke_width=5)
        self.play(Create(mantener), FadeIn(legend[1]), run_time=1.4, rate_func=smooth)

        # Curva total: (D/Q)*S + (Q/2)*H -> DARK_FG (forma de U, minimo en Q*)
        total = axes.plot(lambda q: S * D / q + H * q / 2, x_range=[250, 6000],
                          color=DARK_FG, stroke_width=7)
        self.play(Create(total), FadeIn(legend[2]), run_time=1.6, rate_func=smooth)
        self.wait(0.4)

        # --- 4) Payoff POSITIVO: el punto optimo en OLIVA con brillo ---
        q_star = Q_STAR
        costo_star = S * D / q_star + H * q_star / 2
        punto_glow = VGroup(
            Circle(radius=0.34, color=DARK_OLIVA, fill_opacity=0.30, stroke_width=0),
            Circle(radius=0.68, color=DARK_OLIVA, fill_opacity=0.10, stroke_width=0),
        ).move_to(axes.c2p(q_star, costo_star))
        punto = Dot(axes.c2p(q_star, costo_star), color=DARK_OLIVA, radius=0.13)
        vline = DashedLine(
            axes.c2p(q_star, 0), axes.c2p(q_star, costo_star),
            color=DARK_OLIVA, dash_length=0.08, stroke_width=4,
        )
        qlabel = Text("Q* \u00b7 1.549", font=FONT_MONO, font_size=22, color=DARK_OLIVA
                      ).next_to(punto, UR, buff=0.15)
        sello = VGroup(
            Rectangle(width=0.16, height=0.16, fill_color=DARK_OLIVA, stroke_width=0),
            Text("PUNTO OPTIMO \u00b7 EL MAS BARATO", font=FONT_MONO, font_size=21,
                 color=DARK_FG),
        ).arrange(RIGHT, buff=0.25)
        sello.next_to(axes, UP, buff=0.35)

        self.add_sound(BLIP_PROTA)
        self.play(Create(vline), FadeIn(punto_glow), FadeIn(punto, scale=2.0),
                  FadeIn(qlabel), run_time=0.7, rate_func=ease_out_expo)
        self.play(FadeIn(sello, shift=UP * 0.15), run_time=0.4)
        self._ping(punto.get_center(), DARK_OLIVA, 2)
        self.play(punto.animate.scale(1.7), run_time=0.4, rate_func=ease_out_expo)
        self.play(punto.animate.scale(1.0 / 1.7), run_time=0.4, rate_func=smooth)
        self.wait(0.8)

        # --- 5) Cierre ---
        ghost = Text(
            "Q*", font=FONT_DISPLAY, font_size=220, weight=BOLD, color=DARK_FG,
            fill_opacity=GHOST_OPACITY,
        ).to_corner(DR, buff=-0.2)
        titulo = Text(
            "El equilibrio entre ordenar y guardar",
            font=FONT_TITULO, font_size=36, weight=BOLD, color=DARK_FG,
        ).to_corner(UL, buff=1.35)

        self.add_sound(BLIP_CIERRE)
        self.play(FadeIn(ghost), FadeIn(titulo), run_time=0.9)
        self.wait(2.2)

    def _ping(self, point, color, veces=1):
        """Brillo de radar: anillo que se expande y se desvanece (enmarca lo importante)."""
        for _ in range(veces):
            ring = Circle(radius=0.12, color=color, stroke_width=7).move_to(point)
            self.add(ring)
            self.play(ring.animate.scale(3.4).set_opacity(0.0), run_time=0.7,
                      rate_func=ease_out_expo)
            self.remove(ring)
