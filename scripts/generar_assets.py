"""Genera los assets de la demo 3D Data en Criollo (reproducible).

Uso:
  ~/miniforge3/envs/manim/bin/python scripts/generar_assets.py

Crea:
  assets/papel_grain.png  -> textura de papel con grano (fondo)
  assets/blip_col.wav     -> blip de crecimiento de columna (bajo, corto)
  assets/blip_prota.wav   -> blip de iluminacion de protagonista (medio)
  assets/blip_cierre.wav  -> blip de cierre (largo, grave)
"""

import os
import wave

import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

SR = 44100


def generar_grain(path: str) -> None:
    """Textura papel: color --papel + ruido gaussiano fuerte (visible)."""
    rng = np.random.default_rng(7)
    H, W = 1080, 1920
    base = np.array([0xE8, 0xDF, 0xC8])  # --papel (Print Nostalgia)
    img = np.zeros((H, W, 3), np.uint8)
    for c in range(3):
        noise = rng.normal(0, 28, (H, W))
        img[:, :, c] = np.clip(base[c] + noise, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path)
    print("ok:", path)


def generar_blip(path: str, freq: float, dur: float, amp: float, decay: float) -> None:
    """Pulso sintetico low-fi: seno con ataque rapido y decay exponencial."""
    n = int(dur * SR)
    t = np.linspace(0, dur, n, False)
    env = np.exp(-t * decay) * (1 - np.exp(-t * 300))
    seg = (amp * np.sin(2 * np.pi * freq * t) * env).astype(np.float32)
    pcm = (np.clip(seg, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("ok:", path)


def main() -> None:
    generar_grain(os.path.join(ASSETS, "papel_grain.png"))
    generar_blip(os.path.join(ASSETS, "blip_col.wav"), 180, 0.35, 0.5, 10.0)
    generar_blip(os.path.join(ASSETS, "blip_prota.wav"), 330, 0.60, 0.5, 6.0)
    generar_blip(os.path.join(ASSETS, "blip_cierre.wav"), 220, 1.40, 0.45, 3.0)


if __name__ == "__main__":
    main()
