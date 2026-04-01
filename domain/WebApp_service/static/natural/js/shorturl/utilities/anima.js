import { fmtNum } from "./validator.js";

export const animaModule = {
  /* ─── COUNTER ANIMATION ─── */
  animateCount(el, target, duration = 1800) {
    const start = performance.now();
    const from = 0;
    function update(ts) {
      const progress = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = fmtNum(Math.floor(from + (target - from) * eased));
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  },

  /* ─── LOADING BUTTON ─── */
  setButtonLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    const text = btn.querySelector(".btn-text");
    const load = btn.querySelector(".btn-loading");
    btn.disabled = loading;
    if (text) text.classList.toggle("d-none", loading);
    if (load) load.classList.toggle("d-none", !loading);
  },
};
