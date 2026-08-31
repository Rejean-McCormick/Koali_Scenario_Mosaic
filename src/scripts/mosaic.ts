import { paletteBacklightGroups } from '../lib/palette-icons';

const root = document.querySelector<HTMLElement>('[data-mosaic-root]');

if (root) {
  const data = JSON.parse(root.querySelector<HTMLScriptElement>('[data-mosaic-data]')?.textContent ?? '{}');
  const i18n = JSON.parse(root.querySelector<HTMLScriptElement>('[data-mosaic-i18n]')?.textContent ?? '{}');
  const cells = [...root.querySelectorAll<SVGAElement>('[data-scenario-id]')];
  const search = root.querySelector<HTMLInputElement>('[data-mosaic-search]');
  const count = root.querySelector<HTMLOutputElement>('[data-mosaic-result-count]');
  const canvas = root.querySelector<HTMLElement>('[data-mosaic-canvas]');

  const setText = (query:string, value:string) => {
    const element = root.querySelector<HTMLElement>(query);
    if (element) {
      element.textContent = value;
      element.title = value;
    }
  };

  const compact = (values:string[], empty = '—', limit = 3) => {
    if (!values?.length) return empty;
    return values.length > limit
      ? `${values.slice(0,limit).join(' · ')} +${values.length-limit}`
      : values.join(' · ');
  };

  const titleDensity = (value:string) => value.length > 96 ? 'long' : value.length > 72 ? 'medium' : 'short';

  function selectOnly(id:string) {
    cells.forEach((cell) => cell.classList.toggle('is-active', cell.dataset.scenarioId === id));
  }

  function show(id:string) {
    const scenario = data[id];
    if (!scenario) return;
    selectOnly(id);
    if (canvas) canvas.dataset.activeTerritory = scenario.categoryId;
    setText('[data-preview-id]', scenario.id);
    setText('[data-preview-category]', scenario.category);
    setText('[data-preview-title]', scenario.title);
    const title = root.querySelector<HTMLElement>('[data-preview-title]');
    if (title) title.dataset.titleDensity = titleDensity(scenario.title);
    setText('[data-preview-summary]', scenario.summary);
    setText('[data-preview-category-label]', scenario.category);
    setText('[data-preview-pattern]', scenario.pattern);
    setText('[data-preview-scales]', compact(scenario.scales));
    setText('[data-preview-context]', compact(scenario.contexts));
    setText('[data-preview-properties]', compact(scenario.properties, i18n.noneHighlighted, 2));

    const profile = root.querySelector<HTMLElement>('[data-preview-profile]');
    if (profile) profile.dataset.category = scenario.categoryId;

    const image = root.querySelector<HTMLImageElement>('[data-preview-image]');
    if (image) {
      image.src = scenario.image;
      image.alt = scenario.imageAlt;
      image.dataset.imageState = 'scenario';
    }

    const link = root.querySelector<HTMLAnchorElement>('[data-preview-link]');
    if (link) {
      link.href = scenario.href;
      link.hidden = false;
    }

    const activePalette = new Set<string>(scenario.paletteKeys ?? []);
    root.querySelectorAll<HTMLElement>('[data-backlight-key]').forEach((el) => {
      const group = paletteBacklightGroups.find((item) => item.key === el.dataset.backlightKey);
      const active = !!group?.palette.some((key) => activePalette.has(key));
      el.classList.toggle('is-active', active);
      el.setAttribute('aria-label', `${el.querySelector('.tag-label')?.textContent ?? ''}: ${active ? 'active' : 'inactive'}`);
    });

    root.querySelectorAll<HTMLElement>('[data-activity]').forEach((element) => {
      const key = element.dataset.activity!;
      const active = Boolean(scenario.activities[key]);
      element.classList.toggle('is-active', active);
      const label = element.textContent?.trim() ?? key;
      element.setAttribute('aria-label', `${label}: ${active ? i18n.involved : i18n.notCentral}`);
    });
  }

  cells.forEach((cell) => {
    const id = cell.dataset.scenarioId!;
    cell.addEventListener('pointerenter', () => show(id));
    cell.addEventListener('focus', () => show(id));
  });

  search?.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    cells.forEach((cell) => {
      const hit = !query || data[cell.dataset.scenarioId!].search.includes(query);
      cell.classList.toggle('is-filtered-out', !hit);
      if (hit) visible++;
    });
    if (count) count.value = `${visible} ${visible === 1 ? i18n.scenarioSingular : i18n.scenarios}`;
  });

  root.querySelector('[data-mosaic-surprise]')?.addEventListener('click', () => {
    const visible = cells.filter((cell) => !cell.classList.contains('is-filtered-out'));
    if (visible.length) {
      const cell = visible[Math.floor(Math.random() * visible.length)];
      show(cell.dataset.scenarioId!);
      cell.focus({ preventScroll: true });
    }
  });

  root.querySelector('[data-mosaic-reset]')?.addEventListener('click', () => {
    if (search) search.value = '';
    cells.forEach((cell) => cell.classList.remove('is-filtered-out', 'is-active'));
    if (canvas) delete canvas.dataset.activeTerritory;
    if (count) count.value = `${cells.length} ${i18n.scenarios}`;
  });
}

export {};
