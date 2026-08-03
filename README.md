# Manim · Data en Criollo — Demo 3D

Diorama 3D en **Manim** con el sistema de marca **Data en Criollo** (Print Nostalgia).
Demostración del caso Camilo · Bogotá: el margen por día revela que MAR-MIE-JUE
hacen 2/3 del margen → Pareto → +34% en 90 días.

Esto es la prueba de concepto de la fusión: **Manim (3D programático) + marca del vault**.

---

## Parte A — Indicaciones generales (el sistema)

### Qué es esto

- **`dec_brand.py`** — tokens de marca reutilizables (paleta + tipografías + reglas) en Python.
  Única fuente de verdad para Manim. Cualquier escena nueva importa de acá.
- **`camilo_3d.py`** — escena demo: `ThreeDScene` con columnas 3D, cámara, UI de marca
  fija en pantalla, sonido sincronizado y textura de papel.
- **`assets/`** — textura de papel con grano + blips de sonido (generables, ver script).
- **`scripts/generar_assets.py`** — regenera grain + blips (reproducible, semillas fijas).

### Entorno (por qué Miniforge)

Manim (pycairo/manimpango) NO tiene wheels para macOS Intel y requiere compilador.
La vía robusta sin Xcode CLT ni Homebrew: **Miniforge (conda-forge)**, que trae todo
precompilado (Python + cairo + pango + manim como binarios).

### Tipografía

Las 4 familias de la marca deben estar instaladas localmente (Pango/fontconfig las busca
en `~/Library/Fonts`): **Oswald**, **Playfair Display** (± italic), **Source Serif 4**
(± italic), **Cutive Mono**. Se bajan de `github.com/google/fonts`.

### Comandos

```bash
# render a MP4 (con audio)
~/miniforge3/envs/manim/bin/manim render -q m camilo_3d.py CamiloPareto3D

# preview web liviano (960px)
ffmpeg -y -v error -i media/videos/camilo_3d/720p30/CamiloPareto3D.mp4 \
  -vf "scale=960:-1" -c:v libx264 -crf 22 -pix_fmt yuv420p -movflags +faststart -c:a copy camilo_3d_v4.mp4

# regenerar assets
~/miniforge3/envs/manim/bin/python scripts/generar_assets.py
```

### Limitaciones conocidas de Manim 3D (honestidad)

- **Z-fighting / depth sorting**: los objetos que se intersectan pueden "fundirse".
  Regla: evitar intersecciones. (Ver diseño actual: footprints + highlight por desplazamiento).
- **Textura/blend**: no hay `multiply` ni duotono nativo → preprocesar con PIL (patrón del proyecto).
- **Tracking de letras** (labels 0.22em): no nativo → aceptar sin tracking o espaciar a mano.
- **Texto en el espacio 3D se ve mal** → usar `add_fixed_in_frame_mobjects` para la UI.
- **Emojis no renderizan** en Cairo; símbolos (→ ↳ ◆ ✓ ± %) sí.
- **Cámara**: movimientos SUTILES (estilo Johnny Harris / Vox); órbitas agresivas
  producen superposiciones que "fusionan" columnas.

### Siguientes pasos sugeridos

1. Módulo de mobjects de marca reutilizables (filete, wordmark, ghost number, label).
2. Escenas nuevas por pieza: 9:16 Shorts vs 16:9 YouTube vs 1:1 carrusel (definir objetivo).
3. Look 12fps handcrafted: `config.frame_rate = 12`.
4. Voz en off / música real en vez de blips placeholder.
5. Unificar con el sistema Remotion: la paleta de Remotion (`#DAD9D5/#E04329`)
   NO coincide con la marca — elegir UNO (recomendado: el de marca).

---

## Parte B — Indicaciones para hacer ESTA demo (paso a paso)

### 1. Instalar el entorno

```bash
# Miniforge (Intel macOS)
curl -LsSf https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh -o /tmp/miniforge.sh
bash /tmp/miniforge.sh -b -p $HOME/miniforge3

# env con manim (todo binario, sin compilador)
$HOME/miniforge3/bin/conda create -y -n manim -c conda-forge python=3.12 manim

# pillow (para regenerar assets)
$HOME/miniforge3/envs/manim/bin/pip install pillow
```

### 2. Instalar las fuentes de marca

Descargar de `github.com/google/fonts` a `~/Library/Fonts`:
- `ofl/oswald/Oswald[wght].ttf`
- `ofl/playfairdisplay/PlayfairDisplay[wght].ttf` (+ `PlayfairDisplay-Italic[wght].ttf`)
- `ofl/sourceserif4/SourceSerif4[opsz,wght].ttf` (+ `SourceSerif4-Italic[opsz,wght].ttf`)
- `ofl/cutivemono/CutiveMono-Regular.ttf`

### 3. Generar assets

```bash
~/miniforge3/envs/manim/bin/python scripts/generar_assets.py
```

### 4. Renderizar

```bash
~/miniforge3/envs/manim/bin/manim render -q m camilo_3d.py CamiloPareto3D
```

### 5. Cómo está construida la escena (camilo_3d.py)

| Bloque | Qué hace |
|---|---|
| `footprint()` | Casillero en la plataforma del que nace cada columna (evita que "no se vea nacer") |
| `columna_dia()` | Prism 3D con altura = margen del día; bottom apoyado en `Z_PISO` |
| Crecimiento | `Transform(flat, col)` con `ease_out_expo` ("pop" final, curva Vox) + blip sincronizado |
| Cámara | `frame_center` en el diorama; órbita SUTIL (`ambient rate 0.04`); cierre frontal |
| Highlight | Iluminación secuencial (`interpolate` a blanco 55%) + grupo que se adelanta (`shift OUT`) |
| Sonido | `self.add_sound(blip)` ANTES de cada play → sincronización exacta por tiempo de escena |
| Fondo | `ImageMobject(papel_grain.png)` en z lejano + `background_color = PAPEL` |
| UI marca | `add_fixed_in_frame_mobjects`: filete, label Cutive, título Oswald, ghost 67, wordmark |

### Datos de la historia (Camilo · Bogotá)

- Alturas por día: `[3.0, 8.5, 9.5, 7.5, 4.0, 5.0, 5.5]`
- Protagonistas: MAR, MIE, JUE → 67% del margen → Pareto → **+34% en 90 días**
- Colores: `[STEEL, TERRACOTA, MOSTAZA, BURDEOS, TINTA_MED, OLIVA, STEEL]`

---

## Marca

Sistema **Print Nostalgia** (Data en Criollo): papel `#E8DFC8`, tinta `#1C1810`,
terracota `#C0392B` (único acento), Oswald / Playfair / Source Serif 4 / Cutive Mono.
Ver vault de Obsidian: `Data en Criollo/Marca` y `Data en Criollo/Visual`.
