// @ts-nocheck

/* Shared preview layout controller.
   This file intentionally stays valid plain JavaScript so the offline preview
   builder can copy it without maintaining a second implementation. */
(() => {
  const CONTENT_CHANGE_EVENT = 'preview:contentchange';
  const MAX_TITLE_LINES = 2;
  const FIT_ITERATIONS = 7;

  function initPreview(preview) {
    const copy = preview.querySelector('.preview-copy');
    const title = preview.querySelector('[data-preview-title]');
    const palette = preview.querySelector('[data-preview-palette]');
    if (!copy || !title || !palette) return;

    let frame = 0;
    let lastCopyWidth = -1;

    const fitsTitle = () => {
      const lineHeight = Number.parseFloat(getComputedStyle(title).lineHeight);
      return Number.isFinite(lineHeight)
        && title.scrollHeight <= lineHeight * MAX_TITLE_LINES + 1;
    };

    const setTitleSize = (size) => {
      title.style.setProperty('--preview-title-size', `${size}px`);
    };

    function fitTitle() {
      title.title = title.textContent?.trim() || '';
      title.dataset.titleFitting = 'true';
      delete title.dataset.titleClamped;

      title.style.removeProperty('--preview-title-size');
      const maximum = Number.parseFloat(getComputedStyle(title).fontSize);

      title.style.setProperty('--preview-title-size', 'var(--preview-title-min)');
      const minimum = Number.parseFloat(getComputedStyle(title).fontSize);

      if (!Number.isFinite(maximum) || !Number.isFinite(minimum)) {
        delete title.dataset.titleFitting;
        return;
      }

      setTitleSize(maximum);
      if (!fitsTitle()) {
        setTitleSize(minimum);
        if (!fitsTitle()) {
          title.dataset.titleClamped = 'true';
        } else {
          let low = minimum;
          let high = maximum;
          for (let index = 0; index < FIT_ITERATIONS; index += 1) {
            const candidate = (low + high) / 2;
            setTitleSize(candidate);
            if (fitsTitle()) low = candidate;
            else high = candidate;
          }
          setTitleSize(Math.max(minimum, low - 0.1));
        }
      }

      delete title.dataset.titleFitting;
    }

    function fitPalette() {
      palette.classList.remove('is-two-rows');
      const mode = getComputedStyle(palette)
        .getPropertyValue('--preview-palette-fit')
        .trim();
      if (mode !== 'intrinsic') return;

      palette.classList.toggle(
        'is-two-rows',
        palette.scrollWidth > palette.clientWidth + 1,
      );
    }

    function fitLayout() {
      fitTitle();
      fitPalette();
    }

    function requestFit() {
      if (frame) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        frame = 0;
        fitLayout();
      });
    }

    preview.addEventListener(CONTENT_CHANGE_EVENT, requestFit);

    new MutationObserver(requestFit).observe(title, {
      childList: true,
      characterData: true,
      subtree: true,
    });

    if ('ResizeObserver' in window) {
      new ResizeObserver(([entry]) => {
        const width = entry?.contentRect.width ?? copy.clientWidth;
        if (Math.abs(width - lastCopyWidth) <= 0.5) return;
        lastCopyWidth = width;
        requestFit();
      }).observe(copy);
    } else {
      window.addEventListener('resize', requestFit, { passive: true });
    }

    document.fonts?.ready.then(requestFit);
    window.addEventListener('pageshow', requestFit, { passive: true });
    requestFit();
  }

  document.querySelectorAll('.scenario-preview').forEach(initPreview);
})();
