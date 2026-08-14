"""Barras por trimestre — Q1..Q4 con giro de contexto (Data en Criollo).

Arco narrativo (validado con el usuario + Sistema Visual - Graficos Narrativos):
  Acto 1: barras Q1-Q4 crecen a pasos (boil, steps ~12fps) con NUMEROS QUE
          CUENTAN mientras crece el relleno. Q4 (82%) parece el ganador:
          zoom + halo + ping. Rebote al final (overshoot + asentamiento).
  Acto 2: las barras desaparecen, quedan SOLO los Q con sus valores NOMINALES
          EN PLATA que se CUENTAN (0 -> $X,XM). "en plata real, cuanto es?"
  Acto 3: la camara baja; grafico de lineas de los ultimos 5 anos CON ESCALA
          (eje Y numerado, grillas, linea de nivel). Q4 2025 = el MAS BAJO.
  Cierre: "NO TODO ES LO QUE PARECE" — crecimiento (%) != tamano (plata).

Colores: OTROS (familia fria del sistema): teal, dorado, azul para los datos.
Terracota SOLO como senal: filete, barra Q4 y punto 2025 (regla: 1 vez por
pieza = el momento importante). Iluminacion como siempre: halo + ping + scale.

Sin LaTeX: contadores con Text + ReplacementTransform (DecimalNumber usa MathTex).

Run:
  ~/miniforge3/envs/manim/bin/manim render -q m barras_trimestre.py BarrasTrimestre
"""

import os

import numpy as np

from manim import *
from manim.utils.rate_functions import ease_out_expo, smooth, ease_in_out_sine, linear
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

# --- Paleta de esta pieza (otros colores; terracota = senal) ---
T_TEAL = "#5E9494"
T_GOLD = "#E0BE5C"
T_BLUE = "#5C82B5"
T_TERRACOTA = DARK_TERRACOTA   # senal: Q4 + punto 2025 + filete

# --- Layout (16:9, barras gruesas, aire) ---
TRACK_LEFT = -5.0
BAR_W = 9.6
BAR_H = 0.72
BAR_YS = [1.7, 0.4, -0.9, -2.2]       # step 1.3: labels sin encimarse
FRACS = [0.18, 0.36, 0.57, 0.82]      # crecimiento interanual %
MONEY_V = [1.2, 1.6, 2.1, 2.8]        # nominal en plata (millones)
BAR_COLORS = [T_TEAL, T_GOLD, T_BLUE, T_TERRACOTA]
STEPS = 10
STEP_T = 0.24

# Linea: Q4 de los ultimos 5 anos ($ millones) — 2025 es el mas bajo
YEARS = [2021, 2022, 2023, 2024, 2025]
VALS = [6.2, 5.1, 4.4, 3.6, 2.8]


class BarrasTrimestre(ThreeDScene):
    def construct(self):
        self.camera.background_color = DARK_BG
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # --- UI de marca ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=T_TERRACOTA, stroke_width=0
                      ).move_to([-5.9, 3.1, 0]),
            Rectangle(width=3.6, height=0.02, fill_color=DARK_FG, stroke_width=0
                      ).next_to([-5.9 + 0.9 / 2, 3.1, 0], RIGHT, buff=0.0),
        )
        label = Text(
            "VENTAS POR TRIMESTRE \u00b7 CRECIMIENTO %",
            font=FONT_MONO, font_size=22, color=DARK_FG,
        ).to_corner(UL, buff=0.65)
        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=DARK_FG)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=T_TERRACOTA, stroke_width=0)
        wordmark_c = Text(
            "en Criollo", font=FONT_DISPLAY, font_size=25, slant=ITALIC, color=DARK_FG,
        )
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.scale(0.85).to_corner(DL, buff=0.55)

        titulo = Text(
            "VENTAS POR TRIMESTRE",
            font=FONT_TITULO, font_size=42, weight=BOLD, color=DARK_FG,
        ).to_edge(LEFT, buff=1.0).shift(UP * 2.65)

        self.play(FadeIn(filete), FadeIn(label), FadeIn(wordmark), run_time=0.6)
        self.add_sound(BLIP_PROTA)
        self.move_camera(zoom=1.06, frame_center=ORIGIN, run_time=0.9,
                         rate_func=ease_out_expo,
                         added_anims=[FadeIn(titulo, shift=UP * 0.15)])
        self.wait(0.6)

        # =====================================================================
        # ACTO 1 — las barras crecen con numeros que cuentan
        # =====================================================================
        q_labels = ["Q1", "Q2", "Q3", "Q4"]
        bars_group = VGroup()
        valor_q4 = None

        for i, (ql, frac, color, y) in enumerate(zip(q_labels, FRACS, BAR_COLORS, BAR_YS)):
            track = Rectangle(
                width=BAR_W, height=BAR_H,
                stroke_color=DARK_FG, stroke_width=1.5,
                fill_color=DARK_RAISED, fill_opacity=0.28,
            ).move_to([TRACK_LEFT + BAR_W / 2, y, 0])
            fill = Rectangle(
                width=0.01, height=BAR_H, fill_color=color, stroke_width=0,
            ).move_to([TRACK_LEFT, y, 0])
            # halftone: trama de puntos sobre la barra (textura print)
            dots = VGroup(*[
                Circle(radius=0.042, color=DARK_FG, fill_opacity=0.16, stroke_width=0
                       ).move_to([dx, dy, 0])
                for dx in np.arange(TRACK_LEFT + 0.16, TRACK_LEFT + BAR_W - 0.1, 0.24)
                for dy in np.arange(y - BAR_H / 2 + 0.16, y + BAR_H / 2 - 0.14, 0.24)
            ])
            q = Text(ql, font=FONT_MONO, font_size=26, color=DARK_FG
                     ).next_to(track, UP, buff=0.2)
            valor = Text("0%", font=FONT_MONO, font_size=22, color=DARK_FG
                         ).move_to([TRACK_LEFT + 0.4, y, 0])
            bar = VGroup(track, fill, dots, q, valor)
            bars_group.add(bar)

            if i == 2:
                # Q3: la camara avanza hacia las barras
                self.move_camera(zoom=1.14, frame_center=[0.15, -0.05, 0], run_time=1.0,
                                 rate_func=smooth,
                                 added_anims=[FadeIn(bar)])
                self.wait(0.2)
            else:
                self.play(FadeIn(bar), run_time=0.5)
                self.wait(0.15)

            # relleno a pasos (boil) con % que cuenta en la punta
            for s in range(1, STEPS + 1):
                w = frac * BAR_W * s / STEPS
                pct = int(round(frac * 100 * s / STEPS))
                nuevo = Text(f"{pct}%", font=FONT_MONO, font_size=22, color=DARK_FG
                             ).move_to([TRACK_LEFT + w + 0.38, y, 0])
                self.play(
                    fill.animate.stretch_to_fit_width(w).move_to([TRACK_LEFT + w / 2, y, 0]),
                    ReplacementTransform(valor, nuevo),
                    run_time=STEP_T, rate_func=linear,
                )
                valor = nuevo

            # rebote: la barra pasa un poquito y asienta (como en BarChart.mp4)
            w = frac * BAR_W
            over = w * 1.06
            self.play(
                fill.animate.stretch_to_fit_width(over).move_to([TRACK_LEFT + over / 2, y, 0]),
                valor.animate.move_to([TRACK_LEFT + over + 0.38, y, 0]),
                run_time=0.28, rate_func=ease_out_expo,
            )
            self.play(
                fill.animate.stretch_to_fit_width(w).move_to([TRACK_LEFT + w / 2, y, 0]),
                valor.animate.move_to([TRACK_LEFT + w + 0.38, y, 0]),
                run_time=0.28, rate_func=smooth,
            )
            self.wait(0.45)

            if i == 3:
                valor_q4 = valor

        # Climax Q4: zoom + halo + ping (todavia parece el ganador)
        q4_tip = [TRACK_LEFT + FRACS[3] * BAR_W, BAR_YS[3], 0]
        halo_q4 = VGroup(
            Circle(radius=0.34, color=T_TERRACOTA, fill_opacity=0.28, stroke_width=0
                   ).move_to(q4_tip),
            Circle(radius=0.68, color=T_TERRACOTA, fill_opacity=0.10, stroke_width=0
                   ).move_to(q4_tip),
        )
        self.add_sound(BLIP_PROTA)
        self.move_camera(zoom=1.5, frame_center=[1.1, -2.2, 0], run_time=1.0,
                         rate_func=ease_in_out_sine,
                         added_anims=[FadeIn(halo_q4)])
        self._ping(q4_tip, T_TERRACOTA, 2)
        self.play(valor_q4.animate.scale(1.5), run_time=0.4, rate_func=ease_out_expo)
        self.play(valor_q4.animate.scale(1.0 / 1.5), run_time=0.5, rate_func=smooth)
        self.wait(1.1)
        self.move_camera(zoom=1.0, frame_center=ORIGIN, run_time=1.1,
                         rate_func=ease_in_out_sine)
        self.wait(0.4)

        # =====================================================================
        # ACTO 2 — SOLO los Q con su plata contada (sin barras)
        # =====================================================================
        sello_plata = VGroup(
            Rectangle(width=0.16, height=0.16, fill_color=T_GOLD, stroke_width=0),
            Text("EN PLATA REAL, \u00bfCUANTO ES?", font=FONT_MONO, font_size=21,
                 color=DARK_FG),
        ).arrange(RIGHT, buff=0.25).move_to([1.8, 2.25, 0])

        self.move_camera(zoom=1.06, frame_center=[0.8, -0.25, 0], run_time=1.2,
                         rate_func=smooth,
                         added_anims=[FadeOut(bars_group), FadeOut(halo_q4),
                                      FadeIn(sello_plata, shift=UP * 0.15)])
        self.add_sound(BLIP_PROTA)
        self.wait(0.6)

        # lista: Q + contador de plata (0 -> valor)
        LIST_YS = [1.5, 0.4, -0.7, -1.8]
        for i, (ql, m, y) in enumerate(zip(q_labels, MONEY_V, LIST_YS)):
            qlab = Text(ql, font=FONT_MONO, font_size=30, color=DARK_FG
                        ).move_to([-4.3, y, 0])
            self.play(FadeIn(qlab, shift=RIGHT * 0.15), run_time=0.3)
            self.wait(0.1)
            self._contar(m, [1.5, y, 0])
            self.wait(0.35)
        self.wait(0.6)

        # =====================================================================
        # ACTO 3 — la camara baja: grafico de lineas con ESCALA y contexto
        # =====================================================================
        self.move_camera(zoom=1.05, frame_center=[0, -0.75, 0], run_time=1.0,
                         rate_func=smooth,
                         added_anims=[FadeOut(sello_plata)])

        axes = Axes(
            x_range=[2020.5, 2025.5, 1],
            y_range=[0, 7, 1],
            x_length=7.5,
            y_length=2.8,
            axis_config={"color": DARK_FG, "stroke_width": 2,
                         "include_ticks": False, "include_numbers": False},
        ).move_to([0, -0.55, 0])
        chart_label = Text("Q4 \u00b7 ULTIMOS 5 ANOS \u00b7 $ MILLONES",
                           font=FONT_MONO, font_size=18, color=DARK_FG).move_to([0, 1.35, 0])
        ylabel = Text("$ MILLONES", font=FONT_MONO, font_size=16, color=DARK_FG
                      ).next_to(axes, LEFT, buff=0.55).rotate(PI / 2)

        # escala: numeros del eje Y + grillas de contexto
        escala = VGroup()
        grillas = VGroup()
        for v in [0, 2, 4, 6]:
            n = Text(str(v), font=FONT_MONO, font_size=15, color=DARK_FG_MED
                     ).next_to(axes.c2p(2020.5, v), LEFT, buff=0.12)
            g = Line(axes.c2p(2020.5, v), axes.c2p(2025.5, v),
                     color=DARK_FG, stroke_width=1, stroke_opacity=0.10)
            escala.add(n)
            grillas.add(g)

        # linea de nivel del 2025 (el mas bajo)
        nivel = DashedLine(axes.c2p(2020.5, 2.8), axes.c2p(2025, 2.8),
                           color=STEEL, dash_length=0.08, stroke_width=2)

        self.play(Create(axes), FadeIn(chart_label), FadeIn(ylabel), run_time=0.8)
        self.play(FadeIn(escala), FadeIn(grillas), run_time=0.5)
        self.wait(0.2)

        puntos = VGroup()
        lineas = VGroup()
        for i, (yr, v) in enumerate(zip(YEARS, VALS)):
            pt = Dot(axes.c2p(yr, v), radius=0.09, color=DARK_FG)
            yr_lab = Text(str(yr), font=FONT_MONO, font_size=18, color=DARK_FG
                          ).next_to(axes.c2p(yr, 0), DOWN, buff=0.15)
            puntos.add(pt)
            self.play(FadeIn(pt, scale=1.6), FadeIn(yr_lab), run_time=0.35,
                      rate_func=ease_out_expo)
            self.wait(0.1)
            if i > 0:
                seg = Line(axes.c2p(YEARS[i - 1], VALS[i - 1]), axes.c2p(yr, v),
                           color=DARK_FG, stroke_width=3)
                lineas.add(seg)
                self.play(Create(seg), run_time=0.4, rate_func=smooth)
        self.wait(0.4)

        # Revelacion: Q4 2025 = el MAS BAJO (halo + ping + numero protagonista)
        pt2025 = axes.c2p(2025, 2.8)
        halo_2025 = VGroup(
            Circle(radius=0.30, color=T_TERRACOTA, fill_opacity=0.30, stroke_width=0
                   ).move_to(pt2025),
            Circle(radius=0.60, color=T_TERRACOTA, fill_opacity=0.10, stroke_width=0
                   ).move_to(pt2025),
        )
        big_num = Text("$2,8M", font=FONT_DISPLAY, font_size=88, weight=BOLD,
                       color=T_TERRACOTA).next_to(pt2025, RIGHT, buff=0.35)
        sello_bajo = VGroup(
            Rectangle(width=0.16, height=0.16, fill_color=T_TERRACOTA, stroke_width=0),
            Text("2025 \u00b7 EL MAS BAJO EN 5 ANOS", font=FONT_MONO, font_size=21,
                 color=DARK_FG),
        ).arrange(RIGHT, buff=0.25).move_to([0, -2.55, 0])

        self.add_sound(BLIP_PROTA)
        self.play(Create(nivel), FadeIn(halo_2025), puntos[-1].animate.scale(1.6),
                  run_time=0.5, rate_func=ease_out_expo)
        self.play(puntos[-1].animate.scale(1.0 / 1.6), run_time=0.4, rate_func=smooth)
        self._ping(pt2025, T_TERRACOTA, 2)
        self.move_camera(zoom=1.18, frame_center=[axes.c2p(2025, 2.8)[0], -0.55, 0],
                         run_time=0.8, rate_func=ease_in_out_sine,
                         added_anims=[FadeIn(big_num, scale=1.3)])
        self.play(FadeIn(sello_bajo, shift=UP * 0.15), run_time=0.45)
        self.wait(1.4)

        # =====================================================================
        # CIERRE — el contexto lo cambia todo
        # =====================================================================
        self.move_camera(zoom=1.0, frame_center=[0, -0.4, 0], run_time=1.0,
                         rate_func=ease_in_out_sine)
        self.play(FadeOut(VGroup(axes, chart_label, ylabel, escala, grillas, nivel,
                                 puntos, lineas, halo_2025, big_num, sello_bajo)),
                  run_time=0.7)

        ghost = Text(
            "Q4", font=FONT_DISPLAY, font_size=240, weight=BOLD, color=DARK_FG,
            fill_opacity=GHOST_OPACITY,
        ).to_corner(DR, buff=-0.15)
        tagline = Text(
            "NO TODO ES LO QUE PARECE",
            font=FONT_TITULO, font_size=42, weight=BOLD, color=DARK_FG,
        ).move_to([0, -0.3, 0])
        sub = Text(
            "82% DE CRECIMIENTO \u00b7 LA BASE MAS CHICA EN 5 ANOS",
            font=FONT_MONO, font_size=22, color=DARK_FG,
        ).next_to(tagline, DOWN, buff=0.35)

        self.add_sound(BLIP_CIERRE)
        self.play(FadeIn(ghost), FadeIn(tagline, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(2.4)

    # ------------------------------------------------------------------
    def _contar(self, target, pos, steps=14, run=0.8, size=30):
        """Contador sin LaTeX: Text + ReplacementTransform (0 -> target)."""
        txt = Text("$0,0M", font=FONT_MONO, font_size=size, color=DARK_FG).move_to(pos)
        self.play(FadeIn(txt, scale=1.6), run_time=0.2, rate_func=ease_out_expo)
        for i in range(1, steps + 1):
            v = target * i / steps
            s = f"${v:.1f}M".replace(".", ",")
            nuevo = Text(s, font=FONT_MONO, font_size=size, color=DARK_FG).move_to(pos)
            self.play(ReplacementTransform(txt, nuevo), run_time=run / steps,
                      rate_func=linear)
            txt = nuevo
        return txt

    def _ping(self, point, color, veces=1):
        """Brillo de radar: anillo que se expande y se desvanece."""
        for _ in range(veces):
            ring = Circle(radius=0.12, color=color, stroke_width=7).move_to(point)
            self.add(ring)
            self.play(ring.animate.scale(3.4).set_opacity(0.0), run_time=0.7,
                      rate_func=ease_out_expo)
            self.remove(ring)
