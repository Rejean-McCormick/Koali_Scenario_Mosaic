import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(SplitText);

type CharState = {
  el: HTMLElement;
  restX: number;
  restY: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  targetX: number;
  targetY: number;
};

export const TERRITORY_REPULSION_DEFAULTS = {
  radiusDesktop: 104,
  maxOffset: 11,
  forceExponent: 1.95,
  spring: 0.085,
  damping: 0.56,
  pointerSmoothing: 0.34,
  maxVelocity: 1.35,
  settleDistance: 0.06,
  settleVelocity: 0.05,
};

const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function initTerritoryRepulsion(canvas: HTMLElement) {
  if (!finePointer.matches || reducedMotion.matches) return () => {};

  const lines = [...canvas.querySelectorAll<HTMLElement>('[data-territory-line]')];
  if (!lines.length) return () => {};

  const splitInstances: SplitText[] = [];
  const states: CharState[] = [];
  const pointer = { x: 0, y: 0, rawX: 0, rawY: 0, active: false, initialized: false };
  let tickerRunning = false;
  let visible = true;
  let destroyed = false;
  let measureFrame = 0;

  try {
    for (const line of lines) {
      const split = SplitText.create(line, {
        type: 'chars',
        charsClass: 'territory-label__char',
        tag: 'span',
        aria: 'hidden',
      });
      splitInstances.push(split);
      for (const char of split.chars as HTMLElement[]) {
        states.push({ el: char, restX: 0, restY: 0, x: 0, y: 0, vx: 0, vy: 0, targetX: 0, targetY: 0 });
      }
    }
  } catch (error) {
    console.warn('Koali territory labels: static fallback enabled.', error);
    splitInstances.forEach((instance) => instance.revert());
    return () => {};
  }

  const measure = () => {
    if (destroyed) return;
    const canvasRect = canvas.getBoundingClientRect();
    for (const state of states) {
      const rect = state.el.getBoundingClientRect();
      state.restX = rect.left + rect.width / 2 - canvasRect.left - state.x;
      state.restY = rect.top + rect.height / 2 - canvasRect.top - state.y;
    }
  };

  const scheduleMeasure = () => {
    cancelAnimationFrame(measureFrame);
    measureFrame = requestAnimationFrame(measure);
  };

  const settled = () => states.every((state) =>
    Math.abs(state.x) < TERRITORY_REPULSION_DEFAULTS.settleDistance &&
    Math.abs(state.y) < TERRITORY_REPULSION_DEFAULTS.settleDistance &&
    Math.abs(state.vx) < TERRITORY_REPULSION_DEFAULTS.settleVelocity &&
    Math.abs(state.vy) < TERRITORY_REPULSION_DEFAULTS.settleVelocity
  );

  const sleep = () => {
    if (!tickerRunning) return;
    gsap.ticker.remove(tick);
    tickerRunning = false;
  };

  const wake = () => {
    if (tickerRunning || destroyed || !visible) return;
    gsap.ticker.add(tick);
    tickerRunning = true;
  };

  function tick() {
    if (!visible || destroyed) {
      sleep();
      return;
    }

    const frameFactor = Math.min(2, Math.max(0.5, gsap.ticker.deltaRatio(60)));
    const damping = Math.pow(TERRITORY_REPULSION_DEFAULTS.damping, frameFactor);

    if (pointer.active) {
      if (!pointer.initialized) {
        pointer.x = pointer.rawX;
        pointer.y = pointer.rawY;
        pointer.initialized = true;
      } else {
        const follow = 1 - Math.pow(1 - TERRITORY_REPULSION_DEFAULTS.pointerSmoothing, frameFactor);
        pointer.x += (pointer.rawX - pointer.x) * follow;
        pointer.y += (pointer.rawY - pointer.y) * follow;
      }
    }

    for (const state of states) {
      if (pointer.active) {
        const dx = state.restX - pointer.x;
        const dy = state.restY - pointer.y;
        const distance = Math.hypot(dx, dy);
        if (distance > 0.001 && distance < TERRITORY_REPULSION_DEFAULTS.radiusDesktop) {
          const proximity = Math.max(0, 1 - distance / TERRITORY_REPULSION_DEFAULTS.radiusDesktop);
          const force = Math.pow(proximity, TERRITORY_REPULSION_DEFAULTS.forceExponent);
          const amount = TERRITORY_REPULSION_DEFAULTS.maxOffset * force;
          state.targetX = (dx / distance) * amount;
          state.targetY = (dy / distance) * amount;
        } else {
          state.targetX = 0;
          state.targetY = 0;
        }
      } else {
        state.targetX = 0;
        state.targetY = 0;
      }

      state.vx += (state.targetX - state.x) * TERRITORY_REPULSION_DEFAULTS.spring * frameFactor;
      state.vy += (state.targetY - state.y) * TERRITORY_REPULSION_DEFAULTS.spring * frameFactor;
      state.vx *= damping;
      state.vy *= damping;
      const maxV = TERRITORY_REPULSION_DEFAULTS.maxVelocity;
      state.vx = Math.max(-maxV, Math.min(maxV, state.vx));
      state.vy = Math.max(-maxV, Math.min(maxV, state.vy));
      state.x += state.vx * frameFactor;
      state.y += state.vy * frameFactor;

      if (!pointer.active && Math.abs(state.x) < 0.01 && Math.abs(state.y) < 0.01 && Math.abs(state.vx) < 0.01 && Math.abs(state.vy) < 0.01) {
        state.x = state.y = state.vx = state.vy = 0;
      }

      gsap.set(state.el, { x: state.x, y: state.y, force3D: true });
    }

    if (!pointer.active && settled()) sleep();
  }

  const onPointerMove = (event: PointerEvent) => {
    const rect = canvas.getBoundingClientRect();
    pointer.rawX = event.clientX - rect.left;
    pointer.rawY = event.clientY - rect.top;
    if (!pointer.active) {
      pointer.x = pointer.rawX;
      pointer.y = pointer.rawY;
      pointer.initialized = true;
    }
    pointer.active = true;
    wake();
  };

  const onPointerLeave = () => {
    pointer.active = false;
    pointer.initialized = false;
    wake();
  };

  const resetImmediately = () => {
    pointer.active = false;
    pointer.initialized = false;
    for (const state of states) {
      state.x = state.y = state.vx = state.vy = state.targetX = state.targetY = 0;
      gsap.set(state.el, { x: 0, y: 0 });
    }
    sleep();
  };

  const resizeObserver = new ResizeObserver(scheduleMeasure);
  resizeObserver.observe(canvas);

  const intersectionObserver = new IntersectionObserver((entries) => {
    visible = Boolean(entries[0]?.isIntersecting);
    if (!visible) resetImmediately();
    else scheduleMeasure();
  }, { threshold: 0.01 });
  intersectionObserver.observe(canvas);

  canvas.addEventListener('pointermove', onPointerMove, { passive: true });
  canvas.addEventListener('pointerleave', onPointerLeave, { passive: true });

  document.fonts?.ready.then(scheduleMeasure).catch(scheduleMeasure);
  scheduleMeasure();

  const cleanup = () => {
    if (destroyed) return;
    destroyed = true;
    cancelAnimationFrame(measureFrame);
    canvas.removeEventListener('pointermove', onPointerMove);
    canvas.removeEventListener('pointerleave', onPointerLeave);
    resizeObserver.disconnect();
    intersectionObserver.disconnect();
    sleep();
    splitInstances.forEach((instance) => instance.revert());
  };

  document.addEventListener('astro:before-swap', cleanup, { once: true });
  return cleanup;
}

const canvas = document.querySelector<HTMLElement>('[data-mosaic-canvas]');
if (canvas) initTerritoryRepulsion(canvas);
