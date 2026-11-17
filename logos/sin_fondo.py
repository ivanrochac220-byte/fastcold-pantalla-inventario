import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(float)
h, w, _ = im.shape
bg = np.median(np.concatenate([im[:10,:10].reshape(-1,3), im[:10,-10:].reshape(-1,3), im[-10:,:10].reshape(-1,3), im[-10:,-10:].reshape(-1,3)]), axis=0)
# color-to-alpha: el logo es más oscuro que el fondo
a = np.max((bg - im) / bg, axis=2).clip(0, 1)
a = ((a - .06) / .94).clip(0, 1)          # quita el ruido del JPG
a = np.minimum(1, a * 1.15)               # bordes firmes
safe = np.where(a > 0, a, 1)[..., None]
col = ((im - (1 - a[..., None]) * bg) / safe).clip(0, 255)
assert 0 <= a.min() and a.max() <= 1, 'alfa fuera de rango'
ys, xs = np.where(a > .02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
a, col = a[y0:y1, x0:x1], col[y0:y1, x0:x1]
verde = col[..., 1] > col[..., 2]          # el lema es verde; la letra script, azul
def guarda(rgb, nombre):
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
    img = Image.fromarray(rgba, 'RGBA'); img = img.resize((1100, round(1100 * img.height / img.width)), Image.LANCZOS)
    img.save(f'{out}/{nombre}', optimize=True); print(nombre, img.size)
guarda(col, 'logo-color.png')
neg = np.empty_like(col); neg[:] = (255, 255, 255); neg[verde] = (0x6C, 0xD9, 0x74)
guarda(neg, 'logo-negativo.png')
