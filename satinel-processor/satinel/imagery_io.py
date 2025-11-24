from pathlib import Path
from PIL import Image
import numpy as np


def load_image(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return Image.open(p)


def save_overlay(img: Image.Image, outpath: str):
    p = Path(outpath)
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)


def load_mask(path: str):
    return np.load(path)
