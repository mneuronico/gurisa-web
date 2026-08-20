"""
Reemplaza la portada incrustada dentro de una tarjeta ya compuesta.

Las tarjetas de partes/Capitulo*.webp tienen la portada del capitulo horneada
adentro, con el marco amarillo y los demas adornos dibujados encima. Este
script encuentra donde y a que escala quedo la portada vieja -por correlacion
contra la propia tarjeta-, arma la mascara de los pixeles que son portada y no
adorno, y pega la portada nueva solo ahi.

El canal alpha no se toca, asi que la silueta de la carpeta y el redondeo de
las esquinas se conservan exactos.

  python tools/hornear_portada.py <tarjeta.webp> <portada_vieja> <portada_nueva> <salida.webp>
"""
import sys
import numpy as np
import cv2
from PIL import Image


def _bgr(p):
    return cv2.cvtColor(np.array(Image.open(p).convert('RGB')), cv2.COLOR_RGB2BGR)


def encajar(tarjeta, portada, escalas):
    """Devuelve (score, escala, offset) de la portada dentro de la tarjeta."""
    h, w = tarjeta.shape[:2]
    parche = tarjeta[h // 2 - 60:h // 2 + 60, w // 2 - 60:w // 2 + 60]
    mejor = None
    for s in escalas:
        pr = cv2.resize(portada, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        if pr.shape[0] < parche.shape[0] or pr.shape[1] < parche.shape[1]:
            continue
        _, mx, _, loc = cv2.minMaxLoc(cv2.matchTemplate(pr, parche, cv2.TM_CCOEFF_NORMED))
        if mejor is None or mx > mejor[0]:
            mejor = (mx, s, ((w // 2 - 60) - loc[0], (h // 2 - 60) - loc[1]))
    return mejor


def proyectar(portada, escala, offset, forma):
    """Dibuja la portada escalada sobre un lienzo del tamanio de la tarjeta."""
    pr = cv2.resize(portada, None, fx=escala, fy=escala, interpolation=cv2.INTER_AREA)
    lienzo = np.zeros(forma, np.uint8)
    dentro = np.zeros(forma[:2], bool)
    ox, oy = offset
    x0, y0 = max(ox, 0), max(oy, 0)
    x1, y1 = min(ox + pr.shape[1], forma[1]), min(oy + pr.shape[0], forma[0])
    lienzo[y0:y1, x0:x1] = pr[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
    dentro[y0:y1, x0:x1] = True
    return lienzo, dentro


def hornear(ruta_tarjeta, ruta_vieja, ruta_nueva, tolerancia=26):
    rgba = np.array(Image.open(ruta_tarjeta).convert('RGBA'))
    tarjeta = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
    vieja, nueva = _bgr(ruta_vieja), _bgr(ruta_nueva)

    score, s, off = encajar(tarjeta, vieja, np.arange(0.20, 0.75, 0.005))
    score, s, off = encajar(tarjeta, vieja, np.arange(s - 0.006, s + 0.006, 0.0005))
    if score < 0.9:
        raise SystemExit(f'no se encontro la portada vieja en la tarjeta (score {score:.3f})')

    proy_vieja, dentro = proyectar(vieja, s, off, tarjeta.shape)
    proy_nueva, _ = proyectar(nueva, s, off, tarjeta.shape)

    # Son portada los pixeles que coinciden con la vieja; el resto es adorno
    # dibujado encima (marco amarillo, personajes) y se deja intacto.
    parecido = np.abs(tarjeta.astype(int) - proy_vieja.astype(int)).max(axis=2) <= tolerancia
    mascara = parecido & dentro & (rgba[:, :, 3] > 0)
    # Cierra los agujeritos que deja el ruido de compresion.
    mascara = cv2.morphologyEx(mascara.astype(np.uint8), cv2.MORPH_CLOSE,
                               np.ones((5, 5), np.uint8)).astype(bool)
    mascara &= dentro

    salida = tarjeta.copy()
    salida[mascara] = proy_nueva[mascara]
    rgba[:, :, :3] = cv2.cvtColor(salida, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgba, 'RGBA'), score, s, off, float(mascara.mean())


if __name__ == '__main__':
    tarjeta, vieja, nueva, salida = sys.argv[1:5]
    im, score, s, off, cobertura = hornear(tarjeta, vieja, nueva)
    im.save(salida, lossless=True, method=6)
    print(f'{salida}: score {score:.4f} escala {s:.4f} offset {off} '
          f'| {cobertura*100:.1f}% del lienzo reemplazado')
