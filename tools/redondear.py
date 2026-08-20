"""
Redondea las esquinas convexas de la silueta de una imagen con alpha.

Es una apertura morfologica (erosion + dilatacion) con un disco de radio r:
sobre una silueta con lados rectos, los lados quedan intactos y solo las
esquinas salientes se redondean con ese radio. Las esquinas entrantes -como
el encuentro entre la pestania y el cuerpo de la carpeta- quedan como estan,
que es lo que uno espera de una carpeta.
"""
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt


def redondear(im, r):
    alpha = np.array(im.convert('RGBA'))[:, :, 3]
    # Margen para que el disco no se corte contra el borde del lienzo.
    pad = int(r) + 2
    solido = np.pad(alpha > 128, pad, constant_values=False)

    # Erosion: sobrevive lo que esta a mas de r del fondo.
    erosionado = distance_transform_edt(solido) >= r
    # Dilatacion con antialias: cobertura segun la distancia al set erosionado.
    d = distance_transform_edt(~erosionado)
    cobertura = np.clip(r + 0.5 - d, 0, 1)[pad:-pad, pad:-pad]

    salida = np.array(im.convert('RGBA'))
    salida[:, :, 3] = (alpha * cobertura).astype(np.uint8)
    return Image.fromarray(salida, 'RGBA')


if __name__ == '__main__':
    origen, destino, radio = sys.argv[1], sys.argv[2], float(sys.argv[3])
    redondear(Image.open(origen), radio).save(destino, lossless=True, method=6)
