# CLAUDE.md — Data en Criollo Manim Motion Graphics

Instructions for Claude Code (and any AI) working in this repo.

## What this project is

Cinematic motion graphics for **Data en Criollo** — an Argentine data-education
brand (YouTube/Instagram style, 3Blue1Brown vibes, "Print Nostalgia" visual
identity). Scenes are built with **Manim Community v0.20.1** in a dedicated
conda env. The target audience is non-experts: every piece must be understood
at a glance.

## How to render (MANDATORY — exact commands)

Manim is NOT on PATH. The env is `~/miniforge3/envs/manim`. Always run from
this repo root:

```bash
~/miniforge3/envs/manim/bin/manim render -q m eoq_valle_3d.py EOQValle3D
```

- Output MP4 lands in `media/videos/<scene>/720p30/<Scene>.mp4` (media/ is gitignored).
- **Validate fast first**: `~/miniforge3/envs/manim/bin/manim render -q l -s eoq_valle_3d.py EOQValle3D`
  renders a single last frame and catches API errors in seconds. Use this before every long render.
- Full `-q m` renders are SLOW: 3D camera moves cost ~2.5–3.5 s per frame
  (every frame recomputes the surface). A ~30 s scene takes 25–35 min. Set
  generous timeouts; prefer background rendering with a log file.
- Audio assets live in `assets/` (`blip_prota.wav`, `blip_cierre.wav`).

## Brand system (read `dec_brand.py` — do not hardcode colors)

Dark mode (on `DARK_BG = #1C1810`):

| Token | Hex | Meaning |
|-------|-----|---------|
| DARK_FG | #E8DFC8 | text / paper |
| DARK_FG_MED | #DDD4B8 | secondary text |
| DARK_RAISED | #3D3D38 | raised surfaces |
| DARK_TERRACOTA | #D6452F | signal accent — use ONCE per piece (brand filete) |
| DARK_MOSTAZA | #E0A250 | second accent, highlights |
| DARK_OLIVA | #A8BE8A | POSITIVE / confirmation (optimal, good path) |
| DARK_BURDEOS | #C25B28 | cost / negative emphasis |
| STEEL | #888880 | metadata, labels |

Fonts: `FONT_TITULO` (Oswald, bold uppercase titles), `FONT_MONO` (Cutive Mono,
data/labels ALL CAPS), `FONT_DISPLAY` (Playfair Display, wordmark).
Rules: terracota only for the filete; oliva = the good result (NEVER red for the
optimum); labels in caps mono; fixed-in-frame HUD = filete + label + wordmark.

## Hero scene: `eoq_valle_3d.py` (EOQValle3D)

Concept: total inventory cost as a 3D "heat terrain" — the EOQ optimum is the
**deepest point of a valley**.

- Data: D = 24.000 cajas/año, H = $3/caja/año, S = $150/pedido (hero).
- Surface: cost(Q, S) = (D/Q)·S + (Q/2)·H over Q∈[400,4000], S∈[100,400].
- The valley floor is a "river" of optima Q*(S) = √(2·D·S/H), drawn in olive.
- Hero point: S=$150 → Q* = 1.549 cajas → total cost $4.649.
- Narrative beats: HUD → surface (heat map) → river → establish → orbit → dive
  → sweep along the river → **consequence markers** (Q=400 → $9.600, ordering
  cost explodes; Q=3.500 → $6.279, holding cost explodes) → hero Q* → closing
  "NI POCO NI MUCHO: EL VALLE".
- Business logic to preserve: ordering cost (D/Q)·S grows when Q is small;
  holding cost (Q/2)·H grows when Q is big; the total is their sum; the optimum
  balances both. The 3D S-axis exists to show the optimum MOVES along the valley
  floor when the environment (S) changes.

Related 2D scene: `eoq_supply_chain.py` (same data, formula piece-by-piece).
Source models live in the Obsidian vault:
`Data en Criollo/_Consultoria/_Modelos/Inventarios-Excel/Modelos/`
(`EOQ.md` — animated; `POQ.md`, `Pareto.md`, `Solver.md` — NOT yet animated, natural next scenes).

## CRITICAL gotchas (learned the hard way — do not repeat)

1. **Surfaces MUST map through `axes.c2p()`.** Manim `Surface` expects 3D space
   points, NOT raw range values. Returning `[q, s, cost]` raw builds the surface
   at world coords 200–4000 → it sits out of frame and only the curve (which used
   c2p) is visible. This produced the "solo veo una línea estática" bug.
2. **No LaTeX installed.** `include_numbers=True` on axes uses MathTex → crashes
   with `FileNotFoundError: latex`. Never use `include_numbers`; put values in
   `Text()` labels or fixed-in-frame narrative labels instead.
3. **Manim v0.20 `Create()` does not accept `scale=`** → `TypeError:
   Animation.__init__() got an unexpected keyword argument 'scale'`. Use
   `GrowFromCenter()`.
4. **Fixed-in-frame labels overlap.** Two texts dropped into the same corner
   (e.g. `to_corner(UR)`) overlap each other. Stack with
   `VGroup.arrange(DOWN)` + `next_to(prev, DOWN, aligned_edge=RIGHT)`.
5. **Legibility over spectacle.** Past 3D attempts failed with z-fighting and
   unreadable labels. Use `set_fill_by_value(axes=axes, colorscale=[(color,
   value), ...], axis=2)` for height-based coloring (gives depth without
   z-fighting); keep HUD/labels fixed-in-frame; never place text inside the surface.
6. **Verify what you cannot see.** If the model has no image input, verify
   renders with pixel analysis (PIL): count pixels near brand colors to confirm
   the surface (mostaza/burdeos) and river (oliva) are actually on screen.

## Working style

- Match the brand: dark mode, ALL-CAPS mono labels, Spanish copy (rioplatense).
- Keep scenes SHORT (~30 s). User prefers shorter over fancy.
- After any edit, run the fast `-q l -s` validation before the long render.
- When improving: the user's #1 complaint is CLARITY ("sigo sin entenderlo").
  If in doubt, make the message more explicit (say WHY, not just WHAT).
