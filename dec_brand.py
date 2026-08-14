"""Data en Criollo — brand tokens (Print Nostalgia system).

Uso: from dec_brand import *
Tokens segun el vault (Marca/ + Visual/).
"""

# --- Paleta de colores ---
PAPEL = "#E8DFC8"     # fondo principal, papel crema calido
PAPEL2 = "#DDD4B8"    # cards, secciones secundarias
CREMA = "#F5EDD8"     # superficies elevadas
TINTA = "#1C1810"     # texto principal, bordes
TINTA_MED = "#3D3D38" # cuerpo secundario
STEEL = "#888880"     # labels, metadatos, terciario
TERRACOTA = "#C0392B" # Signal Red — unico acento
MOSTAZA = "#C8843A"   # segundo acento, highlights
OLIVA = "#7A8C5A"     # positivo, confirmacion
BURDEOS = "#8B2E00"   # precios, enfasis calido

# Extras para mapas / piezas tematicas
GOLD = "#D4AF37"
SHIRE = "#5B8C5A"
MORDOR = "#8B0000"
RIVENDELL = "#4A6FA5"

# Bandas VHS (legacy, 7 franjas)
VHS = ["#C0392B", "#D4521A", "#C8843A", "#B5A04A", "#7A8C5A", "#4A7A7A", "#3A5A8A"]

# --- Tipografia (Print Nostalgia) ---
FONT_TITULO = "Oswald"           # titulares, bold condensado, uppercase
FONT_DISPLAY = "Playfair Display"  # display / acento, italic + 900
FONT_CUERPO = "Source Serif 4"   # cuerpo
FONT_MONO = "Cutive Mono"        # datos, labels ALL CAPS

# --- Modo oscuro (inversion semantica; acentos aclarados para legibilidad) ---
DARK_BG = TINTA           # --bg: var(--tinta)
DARK_FG = PAPEL           # --fg: var(--papel)
DARK_FG_MED = PAPEL2      # --fg-secondary: var(--papel2)
DARK_RAISED = TINTA_MED   # --bg-raised: var(--tintaMed)
DARK_BORDER = PAPEL       # --border: var(--papel)
DARK_TERRACOTA = "#D6452F"  # terracota aclarado (Signal Red, una vez por pieza)
DARK_MOSTAZA = "#E0A250"    # segundo acento, highlights
DARK_OLIVA = "#A8BE8A"      # positivo / confirmacion (legible sobre oscuro)
DARK_BURDEOS = "#C25B28"    # precios, enfasis calido (legible sobre oscuro)

# --- Reglas de composicion ---
FILETE_H = 0.12                  # filete de marca: 3px terracota + 1px tinta (escala config)
TRACKING_LABEL = 0.22            # letter-spacing labels (em)
GHOST_OPACITY = 0.05             # numero fantasma
