"""
Reemplaza la portada incrustada dentro de una tarjeta de guia.

Igual que tools/hornear_portada.py, pero para los papeles de las guias, donde
la portada no entra en un rect recto sino rotada y deformada dentro del papel.
La transformacion se recupera por correspondencia de rasgos (SIFT + RANSAC)
entre la portada vieja y la tarjeta, asi que no hay que medir nada a mano.

El canal alpha no se toca: el papel, su marco crema y su sombra se conservan.

  python tools/hornear_guia.py <tarjeta.webp> <portada_vieja> <portada_nueva> <salida.webp>
"""
import sys
import numpy as np
import cv2
from PIL import Image


def _bgr(p):
    return cv2.cvtColor(np.array(Image.open(p).convert('RGB')), cv2.COLOR_RGB2BGR)


def homografia(vieja, tarjeta, esc=0.35):
    """Mapea coordenadas de la portada a coordenadas de la tarjeta."""
    chica = cv2.resize(vieja, None, fx=esc, fy=esc, interpolation=cv2.INTER_AREA)
    sift = cv2.SIFT_create(nfeatures=4000)
    k1, d1 = sift.detectAndCompute(cv2.cvtColor(chica, cv2.COLOR_BGR2GRAY), None)
    k2, d2 = sift.detectAndCompute(cv2.cvtColor(tarjeta, cv2.COLOR_BGR2GRAY), None)
    pares = [a for a, b in cv2.BFMatcher().knnMatch(d1, d2, k=2) if a.distance < 0.75 * b.distance]
    if len(pares) < 20:
        raise SystemExit(f'pocas coincidencias ({len(pares)}) entre la portada vieja y la tarjeta')
    src = np.float32([k1[x.queryIdx].pt for x in pares]).reshape(-1, 1, 2) / esc
    dst = np.float32([k2[x.trainIdx].pt for x in pares]).reshape(-1, 1, 2)
    H, inliers = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
    return H, int(inliers.sum()), len(pares)


def hornear(ruta_tarjeta, ruta_vieja, ruta_nueva, tolerancia=30):
    rgba = np.array(Image.open(ruta_tarjeta).convert('RGBA'))
    tarjeta = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
    vieja, nueva = _bgr(ruta_vieja), _bgr(ruta_nueva)

    H, inliers, total = homografia(vieja, tarjeta)
    alto, ancho = tarjeta.shape[:2]
    proy_vieja = cv2.warpPerspective(vieja, H, (ancho, alto), flags=cv2.INTER_AREA)
    proy_nueva = cv2.warpPerspective(nueva, H, (ancho, alto), flags=cv2.INTER_AREA)
    dentro = cv2.warpPerspective(np.full(vieja.shape[:2], 255, np.uint8), H, (ancho, alto)) > 200

    parecido = np.abs(tarjeta.astype(int) - proy_vieja.astype(int)).max(axis=2) <= tolerancia
    mascara = parecido & dentro & (rgba[:, :, 3] > 0)
    mascara = cv2.morphologyEx(mascara.astype(np.uint8), cv2.MORPH_CLOSE,
                               np.ones((5, 5), np.uint8)).astype(bool)
    # Retrae un pixel el borde para no pisar el antialias del marco crema.
    mascara &= cv2.erode(dentro.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)

    salida = tarjeta.copy()
    salida[mascara] = proy_nueva[mascara]
    rgba[:, :, :3] = cv2.cvtColor(salida, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgba, 'RGBA'), inliers, total, float(mascara.mean())


if __name__ == '__main__':
    tarjeta, vieja, nueva, salida = sys.argv[1:5]
    im, inliers, total, cobertura = hornear(tarjeta, vieja, nueva)
    im.save(salida, lossless=True, method=6)
    print(f'{salida}: {inliers}/{total} inliers | {cobertura*100:.1f}% del lienzo reemplazado')
