# Gurisá y Río — sitio web

Sitio de la serie infantil **Gurisá y Río, entre mates y aventuras**: una página
única donde ver los cinco capítulos y descargar las guías didácticas para el aula.

🌐 **[gurisayrio.com](https://gurisayrio.com)**

---

## Tabla de contenido

- [Descripción](#descripción)
- [Cómo está construido](#cómo-está-construido)
- [Requisitos y dependencias](#requisitos-y-dependencias)
- [Instalación y despliegue](#instalación-y-despliegue)
- [Uso](#uso)
  - [Levantar el sitio localmente](#levantar-el-sitio-localmente)
  - [Reemplazar la portada de un capítulo](#reemplazar-la-portada-de-un-capítulo)
  - [Reemplazar la portada de una guía](#reemplazar-la-portada-de-una-guía)
  - [Redondear las esquinas de una tarjeta](#redondear-las-esquinas-de-una-tarjeta)
  - [Mover o agregar una capa](#mover-o-agregar-una-capa)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Autores y créditos](#autores-y-créditos)
- [Contacto y soporte](#contacto-y-soporte)
- [Referencias complementarias](#referencias-complementarias)
- [Pendientes conocidos del sitio](#pendientes-conocidos-del-sitio)

---

## Descripción

**Gurisá y Río** es una serie de micros infantiles ambientada en Entre Ríos. Este
repositorio contiene el sitio que la acompaña, pensado como una sola página
ilustrada por la que se navega mirando, no leyendo: la gráfica original de la
serie se despliega a pantalla completa y los elementos dibujados —las tarjetas de
los capítulos, los papeles de las guías, los carteles del final— son en sí mismos
los botones.

Qué ofrece:

- **Los cinco capítulos**, cada uno en su tarjeta con la portada real del micro,
  enlazados a YouTube.
- **Las cinco guías para el aula** en PDF, que se abren en un visor dentro de la
  misma página y se pueden descargar.
- **Enlaces a las instituciones** vinculadas al proyecto.

Alcance: es un sitio **estático de una sola página**. No tiene backend, base de
datos, formularios, autenticación ni analítica. Todo el contenido es fijo y se
publica por despliegue.

| # | Capítulo | Ver | Guía |
|---|----------|-----|------|
| 1 | Mil Mundos | [YouTube](https://youtu.be/xgmZ50ChQK0) | `guias/guia-aula-1.pdf` |
| 2 | Paisajes de Río | [YouTube](https://youtu.be/vWThHisS7hY) | `guias/guia-aula-2.pdf` |
| 3 | Hacé Click | [YouTube](https://youtu.be/KFNbEnc6LHw) | `guias/guia-aula-3.pdf` |
| 4 | Tomá distancia | [YouTube](https://youtu.be/b-zdLcTubB0) | `guias/guia-aula-4.pdf` |
| 5 | Más tiempo para jugar | [YouTube](https://youtu.be/6I3HvJMRZm8) | `guias/guia-aula-5.pdf` |

> **❓ PENDIENTE — confirmar los títulos.** Los nombres de los capítulos de la
> tabla se leyeron de las portadas. Si alguno no es el título oficial, corregirlo.

---

## Cómo está construido

Conviene entender tres ideas antes de tocar nada.

**1. La escena es un plano de coordenadas.** Toda la gráfica es una sola escena de
`1921 × 5399` unidades. Cada dibujo es un `<img class="layer">` posicionado en
porcentajes de ese plano mediante variables CSS:

```css
.capitulo-1-img {
  --x: 17.3347%;   /* posición horizontal */
  --y: 43.6933%;   /* posición vertical */
  --w: 22.3842%;   /* ancho */
  --z: 33;         /* orden de apilado */
}
```

Como todo es porcentual, la escena escala a cualquier pantalla sin recalcular
nada. La página se parte en dos tableros: el *hero* ocupa la primera pantalla
completa y el resto arranca en `y=1530`, empalmados con un gradiente para que no
se vea la costura.

**2. Los botones son transparentes y van encima.** Ningún dibujo es clickeable.
Sobre cada uno se apoya un `<a class="hotspot">` invisible, posicionado con las
mismas variables. El atributo `data-target` lo asocia a su dibujo para animar el
hover:

```html
<a class="hotspot capitulo-1" href="https://youtu.be/xgmZ50ChQK0"
   target="_blank" rel="noopener" data-target="capitulo-1-img"
   aria-label="Ver el capitulo 1 en YouTube"></a>
```

`script.js` solo intercepta el click en dos casos: los hotspots de guías (para
abrir el visor de PDF) y los que todavía son marcadores de posición con
`href="#"`. Cualquier hotspot con un enlace real navega normalmente.

**3. Las portadas están horneadas dentro de las tarjetas.** Esto sorprende y es
importante: los archivos de `portadas/` **no los sirve el sitio**. Son la fuente
que quedó compuesta dentro de `partes/Capitulo*.webp` y `partes/Guia*.webp`, con
el marco y los adornos dibujados encima. Reemplazar un archivo de `portadas/` no
cambia nada en pantalla hasta rehornear la tarjeta con las herramientas de
`tools/` (ver [Uso](#uso)).

---

## Requisitos y dependencias

**Para ver o editar el sitio: nada.** No hay build, ni bundler, ni gestor de
paquetes, ni framework. Son HTML, CSS y JavaScript sin dependencias. Alcanza con
cualquier servidor estático.

- **Navegador**: cualquiera con soporte de WebP animado y `aspect-ratio`
  (Chrome/Edge 88+, Firefox 89+, Safari 15+).
- **Servidor local**: Python 3 trae uno incorporado y ya está configurado en el
  repositorio.

**Para las herramientas de `tools/`** (solo si vas a regenerar imágenes):

| Componente | Versión probada |
|---|---|
| Python | 3.13 |
| NumPy | 2.4 |
| SciPy | 1.18 |
| OpenCV (`opencv-python`) | 4.13 |
| Pillow | 12.0 |

```bash
pip install numpy scipy opencv-python pillow
```

---

## Instalación y despliegue

### Instalación

```bash
git clone https://github.com/mneuronico/gurisa-web.git
```

```bash
cd gurisa-web && python -m http.server 4173
```

Abrir <http://localhost:4173>. No hay paso de instalación de dependencias porque
el sitio no tiene ninguna.

> Servir por HTTP y no abrir `index.html` con doble clic: el visor de PDF usa un
> `<iframe>` que no funciona bien desde `file://`.

### Despliegue

El sitio se publica con **GitHub Pages** desde la raíz de la rama `main`. El
despliegue es automático: **cada push a `main` republica el sitio**, sin acción
manual ni pipeline de CI.

```bash
git push origin main
```

El dominio propio se configura con el archivo [`CNAME`](CNAME) de la raíz, que
contiene `gurisayrio.com`. El DNS del dominio (registrado en Namecheap) apunta al
apex con cuatro registros `A` a las IP de GitHub Pages, más un `CNAME` de `www`
a `mneuronico.github.io`. El certificado HTTPS lo emite y renueva GitHub.

Para verificar que un despliegue salió bien:

```bash
gh api repos/mneuronico/gurisa-web/pages/builds/latest --jq '.status, .commit'
```

---

## Uso

### Levantar el sitio localmente

```bash
python -m http.server 4173
```

### Reemplazar la portada de un capítulo

Las portadas están horneadas dentro de las tarjetas, así que no alcanza con
cambiar el archivo fuente. El script ubica la portada vieja dentro de la tarjeta
por correlación, y reemplaza solo esos píxeles: el marco amarillo, la pestaña
"CAPÍTULO N" y el canal alfa (o sea el redondeo de las esquinas) quedan intactos.

```bash
python tools/hornear_portada.py partes/Capitulo2.webp portada_vieja.png portadas/capitulo-2.png partes/Capitulo2.webp
```

La portada nueva debe ser **1920×1080**, igual que la que reemplaza. Como
argumento `portada_vieja` va la que está horneada hoy; si ya la sobrescribiste,
se recupera del historial:

```bash
git show 6145b6f:portadas/capitulo-2.jpg > portada_vieja.jpg
```

### Reemplazar la portada de una guía

En los papeles de las guías la portada va rotada dentro del dibujo, así que la
transformación se recupera con una homografía (SIFT + RANSAC) en vez de por
correlación directa. El uso es idéntico:

```bash
python tools/hornear_guia.py partes/Guia5.webp guia5_vieja.png portadas/portadas_para_guias_didacticas/cap5.png partes/Guia5.webp
```

### Redondear las esquinas de una tarjeta

Si reexportás una tarjeta desde el archivo de diseño, pierde el redondeo. Se
recupera con una apertura morfológica sobre el canal alfa, que redondea las
esquinas salientes dejando los lados rectos intactos:

```bash
python tools/redondear.py partes/Capitulo1.webp partes/Capitulo1.webp 40
```

El último argumento es el radio en píxeles del asset. El valor en uso es **40**.

### Mover o agregar una capa

1. Agregar el `<img class="layer mi-capa">` en `index.html`, en el orden que
   corresponda dentro de la escena.
2. Definir `--x`, `--y`, `--w` y `--z` en `styles.css`, en porcentajes de la
   escena de 1921 unidades de ancho.
3. Si tiene que ser clickeable, agregar el `<a class="hotspot mi-capa-boton">`
   con las mismas coordenadas más `--h`, y su `data-target`.

---

## Estructura del repositorio

```
gurisa-web/
├── index.html          Toda la página: capas, hotspots y visor de PDF
├── styles.css          Coordenadas de cada capa, animaciones y responsive
├── script.js           Hover de los hotspots y visor de PDF
├── CNAME               Dominio propio para GitHub Pages
├── guias/              Las 5 guías para el aula en PDF (esto sí lo sirve el sitio)
├── partes/             Las capas de la escena (WebP y PNG con transparencia)
├── portadas/           FUENTE de las portadas: no se sirve, se hornea en partes/
├── tools/              Scripts de regeneración de imágenes
└── video/              Material de origen del título animado
```

---

## Contribuciones

> **❓ PENDIENTE — definir.** El repositorio no tiene `CONTRIBUTING.md`. Hay que
> decidir si el proyecto acepta contribuciones externas o es de desarrollo
> cerrado del equipo. Si acepta, conviene crear el archivo y enlazarlo acá.

Mientras tanto, el flujo de trabajo del equipo es: rama `main`, commit y push
directo. Cada push publica en producción, así que conviene verificar los cambios
en local antes de subirlos.

---

## Licencia

> **❓ PENDIENTE — elegir licencia.** Falta decidirla y agregar el archivo
> `LICENSE` en la raíz.
>
> Vale la pena tratar dos cosas por separado, porque una sola licencia no encaja
> bien en este repositorio:
>
> - **El código** (`index.html`, `styles.css`, `script.js`, `tools/`): acá sí
>   aplica una licencia de software tipo MIT, Apache 2.0 o GPL.
> - **La obra audiovisual y gráfica** (ilustraciones de `partes/`, portadas,
>   guías en PDF, los personajes): MIT o Apache **no** son adecuadas, son
>   licencias de software. Para contenido creativo corresponde una Creative
>   Commons, o directamente "todos los derechos reservados" si la productora
>   quiere conservarlos.
>
> Preguntas concretas: ¿qué licencia querés para el código? ¿Y para la gráfica y
> las guías? ¿Quién es el titular de los derechos de la serie?

---

## Autores y créditos

> **❓ PENDIENTE — completar.** Faltan los datos reales. Los necesito para
> escribir esta sección:
>
> - ¿Quiénes son los autores de la serie y qué rol tuvo cada uno? (guion,
>   dirección, ilustración, animación, música, producción)
> - ¿Quién desarrolló el sitio?
> - ¿Cuál es la productora o institución responsable del proyecto?
> - En el repositorio hay un archivo de diseño llamado
>   `ERZONAUTAS_grafica web_V3.ai`. ¿"Erzonautas" es el estudio de diseño, el
>   nombre interno del proyecto, u otra cosa?
> - El sitio enlaza a **Enersa**, **Turismo Entre Ríos** y **Mi Entre Ríos**.
>   ¿Son auspiciantes, coproductores, o simplemente enlaces de interés? Según
>   cuál sea, corresponde acreditarlos acá.

---

## Contacto y soporte

> **❓ PENDIENTE — completar.** Me faltan los canales reales:
>
> - ¿Qué correo de contacto va publicado?
> - ¿Cuál es el canal de YouTube de la serie? (tengo los enlaces de los cinco
>   capítulos, pero no el canal)
> - ¿Hay redes sociales del proyecto?
> - Para docentes que quieran consultar por las guías, ¿hay algún contacto
>   distinto del general?

Para reportar un problema técnico del sitio, abrir un issue en
<https://github.com/mneuronico/gurisa-web/issues>.

---

## Referencias complementarias

- **[`tools/redondear.py`](tools/redondear.py)** — redondeo de esquinas sobre el
  canal alfa. El encabezado del archivo explica el método.
- **[`tools/hornear_portada.py`](tools/hornear_portada.py)** — reemplazo de
  portadas en rect recto.
- **[`tools/hornear_guia.py`](tools/hornear_guia.py)** — reemplazo de portadas en
  rect rotado.
- **Guías para el aula** — los cinco PDF de `guias/`, que son también el material
  didáctico que descarga el público.
- **Historial de commits** — los mensajes documentan en detalle las decisiones de
  composición de la escena, el empalme entre tableros y el tratamiento del título
  animado. Es la mejor fuente sobre por qué la gráfica está armada así.

> **❓ PENDIENTE — confirmar si existen.** ¿Hay manual de usuario, manual técnico,
> guía de marca, biblia de personajes o diagramas del proyecto que convenga
> enlazar acá? Si están fuera del repositorio (Drive, Notion), pasame los enlaces.

---

## Pendientes conocidos del sitio

- Los hotspots de **Volti y Amperín**, **Modo Carpincho** y **Jujo aparece**
  siguen con `href="#"`: se ven y animan, pero no llevan a ningún lado.
  *(❓ ¿A dónde tienen que apuntar?)*
- El título animado `partes/titulo_pajaro.webp` pesa **17,3 MB**, cerca del 95%
  del peso de la portada. Está pendiente reemplazarlo por una versión más liviana.
- `index.html` aplica un filtro SVG que corrige el color del título animado,
  porque el WebP actual salió lavado respecto del resto de la gráfica. Cuando se
  regenere el título desde una fuente RGBA limpia, el filtro se puede eliminar.
