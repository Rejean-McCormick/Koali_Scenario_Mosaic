import { publicActivityGroups, type PublicActivityKey } from '../lib/public-profile';

type ScenarioPreview = {
  id: string;
  title: string;
  category: string;
  categoryId: string;
  pattern: string;
  summary: string;
  palette: string[];
  activities: Record<PublicActivityKey, boolean>;
  scales: string[];
  settings: string[];
  contexts: string[];
  properties: string[];
  domains: string[];
  related: string[];
  image: string;
  imageAlt: string;
  href: string;
  search: string;
};

const root = document.querySelector<HTMLElement>('[data-mosaic-root]');
if (root) {
  const raw = root.querySelector<HTMLScriptElement>('[data-mosaic-data]')?.textContent ?? '{}';
  const data: Record<string, ScenarioPreview> = JSON.parse(raw);
  const cells = Array.from(root.querySelectorAll<SVGAElement>('[data-scenario-id]'));
  const search = root.querySelector<HTMLInputElement>('[data-mosaic-search]');
  const count = root.querySelector<HTMLOutputElement>('[data-mosaic-result-count]');
  const surprise = root.querySelector<HTMLButtonElement>('[data-mosaic-surprise]');
  const reset = root.querySelector<HTMLButtonElement>('[data-mosaic-reset]');
  const touchMode = matchMedia('(hover: none), (pointer: coarse)').matches;

  function setText(selector: string, value: string) {
    const el = root.querySelector<HTMLElement>(selector);
    if (el) {
      el.textContent = value;
      el.title = value;
    }
  }

  function escapeHtml(value: string) {
    const div = document.createElement('div');
    div.textContent = value;
    return div.innerHTML;
  }

  function compactList(values: string[], emptyLabel = '—', limit = 3) {
    if (!values.length) return emptyLabel;
    const visible = values.slice(0, limit);
    return values.length > limit
      ? `${visible.join(' · ')} +${values.length - limit}`
      : visible.join(' · ');
  }

  function updateActivitySignature(activities: Record<PublicActivityKey, boolean>) {
    for (const group of publicActivityGroups) {
      const indicator = root.querySelector<HTMLElement>(`[data-activity="${group.key}"]`);
      if (!indicator) continue;
      const active = Boolean(activities[group.key]);
      indicator.classList.toggle('is-active', active);
      indicator.setAttribute('aria-label', `${group.label}: ${active ? 'involved' : 'not central'}`);
    }
  }

  function preloadRelated(s: ScenarioPreview) {
    for (const id of [s.id, ...s.related].slice(0, 5)) {
      const relatedScenario = data[id];
      if (!relatedScenario) continue;
      const image = new Image();
      image.src = relatedScenario.image;
    }
  }

  function show(id: string, { focusCell = false }: { focusCell?: boolean } = {}) {
    const s = data[id];
    if (!s) return;

    setText('[data-preview-id]', s.id);
    setText('[data-preview-category]', s.category);
    setText('[data-preview-title]', s.title);
    setText('[data-preview-summary]', s.summary);
    setText('[data-preview-category-label]', s.category);
    setText('[data-preview-pattern]', s.pattern);
    setText('[data-preview-scales]', compactList(s.scales));
    setText('[data-preview-context]', compactList(s.contexts));
    setText('[data-preview-properties]', compactList(s.properties, 'None highlighted', 2));

    const profile = root.querySelector<HTMLElement>('[data-preview-profile]');
    if (profile) profile.dataset.category = s.categoryId;

    const image = root.querySelector<HTMLImageElement>('[data-preview-image]');
    if (image) {
      if (image.getAttribute('src') !== s.image) image.src = s.image;
      image.alt = s.imageAlt;
    }

    const link = root.querySelector<HTMLAnchorElement>('[data-preview-link]');
    if (link) {
      link.href = s.href;
      link.hidden = false;
    }

    const palette = root.querySelector<HTMLElement>('[data-preview-palette]');
    if (palette) {
      palette.innerHTML = s.palette
        .slice(0, 5)
        .map((value) => `<span class="tag">${escapeHtml(value.replace(/[-_]+/g, ' '))}</span>`)
        .join('');
    }

    updateActivitySignature(s.activities);

    const related = new Set(s.related);
    cells.forEach((cell) => {
      const cellId = cell.dataset.scenarioId!;
      cell.classList.toggle('is-active', cellId === id);
      cell.classList.toggle('is-related', related.has(cellId));
    });

    if (focusCell) {
      root.querySelector<SVGAElement>(`[data-scenario-id="${id}"]`)?.focus({ preventScroll: true });
    }

    preloadRelated(s);
  }

  function clearSelection() {
    cells.forEach((cell) => cell.classList.remove('is-active', 'is-related'));
  }

  function resetAll() {
    if (search) search.value = '';
    cells.forEach((cell) => {
      cell.classList.remove('is-filtered-out');
      cell.removeAttribute('aria-hidden');
      cell.removeAttribute('tabindex');
    });
    if (count) count.value = `${cells.length} scenarios`;
    clearSelection();
  }

  function applySearch(query: string) {
    const needle = query.trim().toLowerCase();
    let visible = 0;

    cells.forEach((cell) => {
      const scenario = data[cell.dataset.scenarioId!];
      const hit = !needle || scenario.search.includes(needle);
      cell.classList.toggle('is-filtered-out', !hit);

      if (hit) {
        visible += 1;
        cell.removeAttribute('aria-hidden');
        cell.removeAttribute('tabindex');
      } else {
        cell.setAttribute('aria-hidden', 'true');
        cell.setAttribute('tabindex', '-1');
      }
    });

    if (count) count.value = `${visible} scenario${visible === 1 ? '' : 's'}`;
  }

  cells.forEach((cell) => {
    const id = cell.dataset.scenarioId!;

    cell.addEventListener('pointerenter', (event) => {
      if ((event as PointerEvent).pointerType !== 'touch') show(id);
    });

    cell.addEventListener('focus', () => show(id));

    cell.addEventListener('click', (event) => {
      if (touchMode) {
        event.preventDefault();
        show(id);
        root.querySelector('[data-preview]')?.scrollIntoView({
          behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
          block: 'start',
        });
      }
    });
  });

  search?.addEventListener('input', () => applySearch(search.value));

  surprise?.addEventListener('click', () => {
    const visible = cells.filter((cell) => !cell.classList.contains('is-filtered-out'));
    if (!visible.length) return;
    const cell = visible[Math.floor(Math.random() * visible.length)];
    show(cell.dataset.scenarioId!, { focusCell: true });
  });

  reset?.addEventListener('click', resetAll);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      clearSelection();
      (document.activeElement as HTMLElement)?.blur?.();
    }
  });
}

export {};
