"""EOQ Cost Valley 3D v2 — Total Inventory Cost Surface (Data en Criollo).

A 3D surface of total inventory cost where the viewer learns the EOQ optimum
is the DEEPEST POINT OF A VALLEY — now with the surface VISIBLE.

v2 fixes (orchestrator audit after user feedback "solo veo una linea estatica"):
- Surface is mapped through axes.c2p() (v1 built it with raw coords -> the
  valley sat out of frame and only the olive river was visible).
- Surface is a HEAT MAP by height: mostaza (cool, low cost) -> burdeos (hot,
  high cost). The valley reads instantly; the olive river is the "good path".
- CONSEQUENCE markers: Q=400 (order too small, ordering cost explodes) and
  Q=3.500 (order too big, holding cost explodes), each with its real total
  cost, vs the hero Q*=1.549 -> $4.649.
- Axes with tick numbers (Q and S).

Data: D = 24.000, H = $3, S = $150 (hero point)
Surface: cost(Q, S) = (D/Q)*S + (Q/2)*H, Q in [400, 4000], S in [100, 400]
Optimal path: Q*(S) = sqrt(2*D*S/H) -> the "river" on the valley floor.
Hero: S = $150 -> Q* = 1.549 cajas, total cost = $4.649.

Run (mp4):
  ~/miniforge3/envs/manim/bin/manim render -q m eoq_valle_3d.py EOQValle3D
"""

import os

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_expo, smooth
from dec_brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
BLIP_PROTA = os.path.join(BASE, "assets/blip_prota.wav")
BLIP_CIERRE = os.path.join(BASE, "assets/blip_cierre.wav")

# --- Data del ejemplo ---
D_VAL = 24000.0   # demanda anual (cajas)
H_VAL = 3.0       # costo de mantener 1 caja 1 anio ($)
S_HERO = 150.0    # costo de ordenar por pedido ($) para el punto heroico

# Rangos para los ejes de la superficie
Q_MIN, Q_MAX = 400.0, 4000.0
S_MIN, S_MAX = 100.0, 400.0

# Hero point calculations
Q_STAR_HERO = int(round((2 * D_VAL * S_HERO / H_VAL) ** 0.5))      # 1549
COSTO_TOTAL_HERO = (D_VAL / Q_STAR_HERO) * S_HERO + (Q_STAR_HERO / 2) * H_VAL  # 4649.0

# Marcadores de "consecuencia" (decisiones NO optimas, al nivel del hero S=150)
Q_BAD_SMALL = 400.0    # pides poco y seguido -> costo de ordenar explota
Q_BAD_BIG = 3500.0     # pides mucho y espaciado -> costo de mantener explota


def costo(q_val, s_val):
    return (D_VAL / q_val) * s_val + (q_val / 2) * H_VAL


def optimal_q(s_val):
    return (2 * D_VAL * s_val / H_VAL) ** 0.5


def fmt_usd(valor):
    """Formato argentino: $4.649"""
    return "${:,}".format(int(round(valor))).replace(",", ".")


class EOQValle3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = DARK_BG

        # --- UI de marca (fija en pantalla) ---
        filete = VGroup(
            Rectangle(width=0.9, height=0.06, fill_color=DARK_TERRACOTA, stroke_width=0).move_to(
                [-5.9, 3.05, 0]
            ),
            Rectangle(width=3.6, height=0.02, fill_color=DARK_FG, stroke_width=0).next_to(
                [-5.9 + 0.9 / 2, 3.05, 0], RIGHT, buff=0.0
            ),
        )

        label = Text(
            "INVENTARIOS \u00b7 SUPPLY CHAIN \u00b7 EOQ 3D",
            font=FONT_MONO,
            font_size=22,
            color=DARK_FG,
        ).to_corner(UL, buff=0.6)

        wordmark_d = Text("DATA", font=FONT_DISPLAY, font_size=30, weight=BOLD, color=DARK_FG)
        divisor = Rectangle(width=0.045, height=0.55, fill_color=DARK_TERRACOTA, stroke_width=0)
        wordmark_c = Text(
            "en Criollo",
            font=FONT_DISPLAY,
            font_size=25,
            slant=ITALIC,
            color=DARK_FG,
        )
        wordmark = VGroup(wordmark_d, divisor, wordmark_c).arrange(RIGHT, buff=0.18)
        wordmark.scale(0.85).to_corner(DL, buff=0.55)

        self.add_fixed_in_frame_mobjects(filete, label, wordmark)
        self.play(FadeIn(filete), FadeIn(label), FadeIn(wordmark), run_time=0.8)

        # --- Ejes 3D (con numeros) ---
        axes = ThreeDAxes(
            x_range=[Q_MIN, Q_MAX, 800],
            y_range=[S_MIN, S_MAX, 100],
            z_range=[0, 25000, 12500],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={
                "font_size": 18,
                "color": DARK_FG,
            },
        ).set_opacity(0.6)

        axes_labels = VGroup(
            Text("Q (Cantidad Pedido)", font=FONT_MONO, font_size=20, color=DARK_FG).next_to(
                axes.x_axis, DOWN, buff=0.3
            ),
            Text("S (Costo por Pedido)", font=FONT_MONO, font_size=20, color=DARK_FG).next_to(
                axes.y_axis, LEFT, buff=0.3
            ).rotate(PI / 2, axis=OUT),
            Text("Costo Total ($)", font=FONT_MONO, font_size=20, color=DARK_FG).next_to(
                axes.z_axis, OUT, buff=0.3
            ).rotate(PI / 2, axis=OUT),
        )
        axes_labels[0].move_to(axes.x_axis.get_end() + DOWN * 0.9 + LEFT * 0.5)
        axes_labels[1].move_to(axes.y_axis.get_end() + LEFT * 1.6 + UP * 0.5)
        axes_labels[2].move_to(axes.z_axis.get_end() + OUT * 1.1 + RIGHT * 0.5)

        self.add(axes, axes_labels)

        # --- Superficie de Costo Total (MAPEADA a los ejes con c2p) ---
        def func(u, v):
            q_val, s_val = u, v
            return axes.c2p(q_val, s_val, costo(q_val, s_val))

        surface = Surface(
            func,
            u_range=[Q_MIN, Q_MAX],
            v_range=[S_MIN, S_MAX],
            resolution=(34, 34),
        )
        surface.set_stroke(width=0.5, opacity=0.15, color=DARK_FG)
        surface.set_opacity(0.85)
        # Mapa de calor por altura: fresco (mostaza) en el fondo, caliente
        # (burdeos) en las laderas. El valle = lo mas fresco.
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[(DARK_MOSTAZA, 3500), (DARK_BURDEOS, 22000)],
            axis=2,
        )

        self.play(Create(surface), run_time=3)
        self.wait(0.4)

        # --- Rio de Optimos (el camino bueno, en oliva) ---
        def optimal_path_func(v):
            s_val = v
            q_val = optimal_q(s_val)
            return axes.c2p(q_val, s_val, costo(q_val, s_val))

        optimal_path = ParametricFunction(
            optimal_path_func,
            t_range=[S_MIN, S_MAX],
            color=DARK_OLIVA,
            stroke_width=6,
        )
        optimal_path.set_z_index(2)

        self.play(Create(optimal_path), run_time=2.5)
        self.wait(0.4)

        # --- Camera Choreography ---

        # 1. Establish: vista amplia del terreno de calor
        self.set_camera_orientation(
            phi=60 * DEGREES,
            theta=-50 * DEGREES,
            frame_center=axes.c2p((Q_MIN + Q_MAX) / 2, (S_MIN + S_MAX) / 2, 5000),
            zoom=0.8,
        )
        self.wait(0.5)

        # 2. Orbit: la forma de valle se revela
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        # 3. Dive: la camara baja al valle
        s_dive = 250.0
        q_dive = optimal_q(s_dive)
        self.move_camera(
            phi=75 * DEGREES,
            theta=-20 * DEGREES,
            frame_center=axes.c2p(q_dive, s_dive, costo(q_dive, s_dive)),
            zoom=1.3,
            run_time=3.0,
            rate_func=ease_in_out_cubic,
        )
        self.wait(0.4)

        # 4. Sweep: viaje por el rio del optimo (2 paradas)
        for s_parada in (130.0, 380.0):
            q_parada = optimal_q(s_parada)
            self.move_camera(
                phi=70 * DEGREES,
                theta=-30 * DEGREES,
                frame_center=axes.c2p(q_parada, s_parada, costo(q_parada, s_parada)),
                zoom=1.4,
                run_time=1.5,
                rate_func=smooth,
            )
        self.wait(0.4)

        # 5. Consecuencias: decisiones malas al nivel del hero (S = $150)
        self.move_camera(
            phi=58 * DEGREES,
            theta=-50 * DEGREES,
            frame_center=axes.c2p(2200, 250, 9000),
            zoom=0.95,
            run_time=2.5,
            rate_func=ease_in_out_cubic,
        )
        self.wait(0.3)

        # Marcador 1: pedis poco y seguido
        cost_bad_small = costo(Q_BAD_SMALL, S_HERO)
        bad_small_dot = Sphere(
            radius=0.09, resolution=16, color=DARK_BURDEOS, fill_opacity=1
        ).move_to(axes.c2p(Q_BAD_SMALL, S_HERO, cost_bad_small))
        self.play(GrowFromCenter(bad_small_dot), run_time=0.6, rate_func=ease_out_expo)
        lbl_bad_small = VGroup(
            Text(
                f"PEDIS POCO Y SEGUIDO \u00b7 Q = 400 \u2192 {fmt_usd(cost_bad_small)}",
                font=FONT_MONO, font_size=20, color=DARK_BURDEOS,
            ),
            Text(
                "COSTO DE ORDENAR SE DISPARA",
                font=FONT_MONO, font_size=16, color=DARK_FG_MED,
            ),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(UR, buff=0.8)
        self.add_fixed_in_frame_mobjects(lbl_bad_small)
        self.play(FadeIn(lbl_bad_small, shift=UP * 0.1), run_time=0.5)
        self.wait(1.5)

        # Marcador 2: pedis mucho y espaciado (se apila debajo del 1, sin pisarse)
        cost_bad_big = costo(Q_BAD_BIG, S_HERO)
        bad_big_dot = Sphere(
            radius=0.09, resolution=16, color=DARK_BURDEOS, fill_opacity=1
        ).move_to(axes.c2p(Q_BAD_BIG, S_HERO, cost_bad_big))
        self.play(GrowFromCenter(bad_big_dot), run_time=0.6, rate_func=ease_out_expo)
        lbl_bad_big = VGroup(
            Text(
                f"PEDIS MUCHO Y ESPACIADO \u00b7 Q = 3.500 \u2192 {fmt_usd(cost_bad_big)}",
                font=FONT_MONO, font_size=20, color=DARK_BURDEOS,
            ),
            Text(
                "COSTO DE MANTENER SE DISPARA",
                font=FONT_MONO, font_size=16, color=DARK_FG_MED,
            ),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        lbl_bad_big.next_to(lbl_bad_small, DOWN, buff=0.3, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(lbl_bad_big)
        self.play(FadeIn(lbl_bad_big, shift=UP * 0.1), run_time=0.5)
        self.wait(1.8)
        self.play(
            FadeOut(lbl_bad_small), FadeOut(lbl_bad_big),
            FadeOut(bad_small_dot), FadeOut(bad_big_dot),
            run_time=0.5,
        )

        # 6. Hero: el fondo del valle, S = $150, Q* = 1.549
        hero_point_3d = axes.c2p(Q_STAR_HERO, S_HERO, COSTO_TOTAL_HERO)
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            frame_center=hero_point_3d,
            zoom=1.9,
            run_time=2.5,
            rate_func=ease_in_out_cubic,
        )
        self.wait(0.3)

        hero_dot = Sphere(
            radius=0.1, resolution=16, color=DARK_OLIVA, fill_opacity=1
        ).move_to(hero_point_3d)
        self.add_sound(BLIP_PROTA)
        self.play(GrowFromCenter(hero_dot), run_time=0.6, rate_func=ease_out_expo)
        self._ping(hero_point_3d, DARK_OLIVA, 2)

        hero_label = VGroup(
            Text(
                f"Q* = {Q_STAR_HERO} \u00b7 {fmt_usd(COSTO_TOTAL_HERO)}",
                font=FONT_MONO, font_size=28, color=DARK_OLIVA,
            ),
            Text(
                "LOS DOS COSTOS SE COMPENSAN",
                font=FONT_MONO, font_size=16, color=DARK_FG_MED,
            ),
        ).arrange(DOWN, buff=0.2, aligned_edge=RIGHT).to_edge(UR, buff=0.8)
        self.add_fixed_in_frame_mobjects(hero_label)
        self.play(FadeIn(hero_label, shift=UP * 0.1), run_time=0.5)
        self.wait(1.8)

        # 7. Pull-back: el mensaje final
        self.add_sound(BLIP_CIERRE)
        self.move_camera(
            phi=50 * DEGREES,
            theta=-70 * DEGREES,
            frame_center=axes.c2p(2200, 250, 5000),
            zoom=0.75,
            run_time=2.5,
            rate_func=ease_in_out_cubic,
        )
        self.begin_ambient_camera_rotation(rate=0.02)

        closing = VGroup(
            Text("NI POCO NI MUCHO", font=FONT_TITULO, font_size=32, weight=BOLD, color=DARK_FG),
            Text(f"Q* = {Q_STAR_HERO} \u00b7 {fmt_usd(COSTO_TOTAL_HERO)} \u00b7 EL VALLE",
                 font=FONT_MONO, font_size=26, color=DARK_OLIVA),
        ).arrange(DOWN, buff=0.35).to_corner(UR, buff=0.9)
        self.add_fixed_in_frame_mobjects(closing)
        self.play(FadeIn(closing, shift=UP * 0.1), run_time=0.8)
        self.wait(2.2)

    def _ping(self, point, color, veces=1):
        """Brillo de radar: anillo que se expande y se desvanece (enmarca lo importante)."""
        for _ in range(veces):
            ring = Sphere(radius=0.1, resolution=16, color=color, stroke_width=0, fill_opacity=0.0).move_to(point)
            self.add(ring)
            self.play(ring.animate.scale(3.4).set_opacity(0.0), run_time=0.7, rate_func=ease_out_expo)
            self.remove(ring)
