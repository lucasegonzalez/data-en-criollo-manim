# Prompt: CS50R "Todo es un vector" + correcciones en data-en-criollo-manim

## Rol
Senior motion designer + ingeniero de Manim. Trabajás sobre el repo
`https://github.com/lucasegonzalez/data-en-criollo-manim` (clonar, revisar, corregir
y crear la visualización nueva). Código, comentarios y textos de pantalla en español
rioplatense neutral (sin jerga anglosajona en el copy).

## Contexto
El repo tiene una demo 3D en Manim con la marca "Data en Criollo" (Print Nostalgia:
periódico 80s-90s). Leé `README.md` completo primero (Parte A general + Parte B
específica). Tu tarea: corregir la demo existente + crear la pieza visual de apoyo
para el video de CS50R.

## Entorno (NO cambiar)
- Manim 0.20.1: `~/miniforge3/envs/manim/bin/manim render -q m <archivo>.py <Escena>`
- Assets regenerables: `scripts/generar_assets.py` (agregá ahí los blips nuevos)
- Fuentes de marca ya instaladas en `~/Library/Fonts`

## Sistema de marca (reglas NO negociables)
- Colores (`dec_brand.py`): papel #E8DFC8, papel2 #DDD4B8, crema #F5EDD8, tinta
  #1C1810, tintaMed #3D3D38, steel #888880, terracota #C0392B (ÚNICO acento),
  mostaza #C8843A, oliva #7A8C5A, burdeos #8B2E00.
- Tipografías: Oswald (titulares), Playfair Display (display), Source Serif 4
  (cuerpo), Cutive Mono (datos/labels).
- Titulares en sentence case (NUNCA ALL CAPS en Oswald); ALL CAPS solo en labels
  Cutive Mono con tracking amplio. Terracota UNA vez por pieza. Fondo NUNCA liso
  (paper grain). Sin gradientes decorativos. UI fija: `add_fixed_in_frame_mobjects`.

## Errores conocidos a corregir (ya diagnosticados)
1. Z-fighting: NUNCA intersectar objetos 3D (depth sorting de Manim los "funde").
2. Audio: NO usar wav pre-calculado; llamar `self.add_sound(blip)` INMEDIATAMENTE
   ANTES de cada `self.play` (tiempo de escena exacto).
3. Cámara: apuntar al contenido con `frame_center`; movimientos SUTILES
   (ambient ~0.04) — estilo Johnny Harris/Vox, no demo reel de Blender.
4. Trap API v0.20: `ease_in_out_cubic` no está en namespace principal (importar de
   `manim.utils.rate_functions`); `interpolate_color` exige `ManimColor`;
   emojis no renderizan (usar → ↳ ◆ ✓ ± %).
5. Verificar en render final: textos no cortados, textura visible sin gritar,
   sonido acompañando cada movimiento.

## El tema CS50R (Semana 1 — Representing Data)

Qué es: curso GRATIS de Harvard "CS50's Introduction to Programming with R"
(instructores Carter Zenke y David Malan). Nuestro video es una review-explicación
en español LATAM: "cómo atravesar los 6 problem sets y qué se aprende de verdad".

CONCEPTO RECTOR de la Semana 1 (la tesis que debe quedar clara):
**"TODO en R es un vector."** Un número es un vector de 1 elemento; una columna de
Excel es un vector de muchos; un data frame es una LISTA DE VECTORES DEL MISMO
LARGO. Excel piensa en celdas; R opera sobre el vector completo, sin loops.

### La escena a crear: "El ticket de Camilo" (60-90s)

Historia (cold open del guion, en clave marca): Camilo, Buenos Aires, compró
47 cosas online (MercadoLibre, Amazon, el super del barrio) y no sabía cuánto
gastó hasta que llegó la tarjeta. La visualización le explica a R cómo pensarlo.

Secuencia de la escena (respetá este arco narrativo):
1. **El ticket**: un ticket de super arrugado (papel crema, tinta, tipografía mono)
   aparece con "47 ITEMS" como ghost number de fondo. Cutive Mono para los montos.
2. **Se desarma en cajitas**: el ticket se descompone en 47 cajitas individuales
   (una por item), con un blip por cajita (sincronizado en vivo).
3. **Una cajita se separa** y se etiqueta: "VECTOR DE 1" (label Cutive ALL CAPS).
   Punchline seca en pantalla: "47 cosas. Una sola cosa para R."
4. **Se alinean** las 47 cajitas; un arco OLIVA #7A8C5A las envuelve →
   `sum(vector)` de una sola pasada. Mostrar el resultado: el total que no
   sabía Camilo (inventá un total realista en ARS, ej. "$187.400").
5. **El ticket se convierte en data frame**: columnas `item · cantidad · precio`
   aparecen como cabecera de tabla; cada columna se ILUMINA ENTERA y aparece
   `$` + nombre de columna → "de la tabla, traeme la columna" (concepto del
   dólar de R, sin mostrarlo aún).
6. **Cierre**: "Saber leer un CSV es un superpoder" + stat:
   "EL 73% DE LAS PYMES EN LATAM NO USA SUS PROPIOS DATOS" (sello de la serie).

### Cómo integrar la resolución de ejercicios (apoyo visual del video)

Agregá una SEGUNDA escena corta ("Pit Stop", 20-30s) que muestra resolver el
ejercicio real del PS1:
- Un data frame de F1: 30 pit stops, columnas `team · driver · time · lap`.
- Las 4 líneas de R se escriben solas (typewriter, 2 frames por carácter) y cada
  resultado aparece en OLIVA al lado:
  `nrow(datos)` → 30 · `min(datos$time)` · `max(datos$time)` · `sum(datos$time)`
- Pattern interrupt (picardía): `max(time)` → "Error: object 'time' not found"
  con glitch, y una flecha que muestra `datos$time` → "ACORDATE DEL DÓLAR"
  (el error que el curso dice que vas a ver 50 veces).
- Paralelismo criollo que cierra: "Camilo cerraba la caja del restaurante los
  domingos a la noche. Con 4 líneas, lo hace antes de que se enfríe el café."

Decisiones de diseño:
- La escena del ticket puede ser 2D (es más un dato de negocio que un concepto
  espacial) — decidí vos con criterio si algo necesita 3D o no; si usás 3D,
  respetá las reglas anti-z-fighting.
- Paleta papel claro (como la demo existente). Si después se hace versión Shorts
  dark, es otro prompt.
- Sonido: blips sincronizados por cajita/columna/línea de código (mismo patrón
  de `add_sound` antes de cada play).

## Entregables
1. Correcciones de los errores conocidos en la demo existente.
2. Las dos escenas nuevas (ticket + pit stop) renderizadas a MP4 y verificadas.
3. `README.md` actualizado (escenas nuevas, cómo correrlas, decisiones tomadas).
4. Commits convencionales (feat:, fix:, docs:, chore:) sin atribución de IA.
5. Resumen final: qué corregiste, qué creaste, decisiones de diseño y por qué.
