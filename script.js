const hotspots = document.querySelectorAll('.hotspot');

function setTargetHover(link, isHovered) {
  const targetClass = link.dataset.target;

  if (!targetClass) {
    return;
  }

  const target = document.querySelector(`.${CSS.escape(targetClass)}`);

  if (target) {
    target.classList.toggle('is-hovered', isHovered);
  }
}

/* Globo de texto del personaje, si el hotspot tiene uno asociado. */
function setGlobo(link, isHovered) {
  const id = link.dataset.globo;

  if (!id) {
    return;
  }

  const globo = document.getElementById(id);

  if (globo) {
    globo.classList.toggle('is-visible', isHovered);
  }
}

/* ---------- PDF viewer ---------- */
const guias = {
  'guia-1-img': { src: 'guias/guia-aula-1.pdf', title: 'Guía para el aula · Micro 1' },
  'guia-2-img': { src: 'guias/guia-aula-2.pdf', title: 'Guía para el aula · Micro 2' },
  'guia-3-img': { src: 'guias/guia-aula-3.pdf', title: 'Guía para el aula · Micro 3' },
  'guia-4-img': { src: 'guias/guia-aula-4.pdf', title: 'Guía para el aula · Micro 4' },
  'guia-5-img': { src: 'guias/guia-aula-5.pdf', title: 'Guía para el aula · Micro 5' },
};

const viewer = document.getElementById('pdf-viewer');
const frame = document.getElementById('pdf-frame');
const titleEl = document.getElementById('pdf-viewer-title');
const downloadEl = document.getElementById('pdf-download');
let lastFocused = null;

function openGuia(guia) {
  lastFocused = document.activeElement;
  titleEl.textContent = guia.title;
  downloadEl.href = guia.src;
  frame.src = `${guia.src}#view=FitH`;
  viewer.hidden = false;
  document.body.classList.add('pdf-open');
  viewer.querySelector('.pdf-viewer__btn--close').focus();
}

function closeViewer() {
  if (viewer.hidden) {
    return;
  }
  viewer.hidden = true;
  frame.src = 'about:blank';
  document.body.classList.remove('pdf-open');
  if (lastFocused && typeof lastFocused.focus === 'function') {
    lastFocused.focus();
  }
}

viewer.querySelectorAll('[data-close]').forEach((el) => {
  el.addEventListener('click', closeViewer);
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeViewer();
  }
});

hotspots.forEach((link) => {
  const mostrar = (visible) => {
    setTargetHover(link, visible);
    setGlobo(link, visible);
  };

  link.addEventListener('pointerenter', () => mostrar(true));
  link.addEventListener('pointerleave', () => mostrar(false));
  link.addEventListener('focus', () => mostrar(true));
  link.addEventListener('blur', () => mostrar(false));

  link.addEventListener('click', (event) => {
    link.classList.add('is-active');
    window.setTimeout(() => link.classList.remove('is-active'), 300);

    const guia = guias[link.dataset.target];
    if (guia) {
      event.preventDefault();
      openGuia(guia);
      return;
    }

    /*
      Los capitulos llevan un href real a YouTube y tienen que navegar. Solo
      frenamos los hotspots que todavia son marcadores de posicion (href="#").
    */
    if (link.getAttribute('href') === '#') {
      event.preventDefault();
    }
  });
});
