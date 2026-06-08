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

hotspots.forEach((link) => {
  link.addEventListener('pointerenter', () => setTargetHover(link, true));
  link.addEventListener('pointerleave', () => setTargetHover(link, false));
  link.addEventListener('focus', () => setTargetHover(link, true));
  link.addEventListener('blur', () => setTargetHover(link, false));

  link.addEventListener('click', (event) => {
    event.preventDefault();
    link.classList.add('is-active');
    window.setTimeout(() => link.classList.remove('is-active'), 300);
  });
});
