export const alertModule = {
  /* ─── SHOW ALERT ─── */
  showAlert(id, msg, type = "danger") {
    const el = document.getElementById(id);
    if (!el) return;
    el.className = `alert alert-${type} py-2 small`;
    el.textContent = msg;
    el.classList.remove("d-none");
  },

  hideAlert(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add("d-none");
  },

  /* ─── TOAST ─── */
  showToast(msg, type = "success") {
    const t = document.createElement("div");
    t.className = `snap-toast ${type}`;
    t.innerHTML = `<i class="fa-solid fa-${
      type === "success" ? "check-circle" : "circle-exclamation"
    } me-2"></i>${msg}`;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3500);
  },
};

/* ─── COPY ─── */
export function copyText(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => alertModule.showToast("Copied to clipboard!"))
    .catch(() => {
      const el = document.createElement("textarea");
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand("copy");
      el.remove();
      alertModule.showToast("Copied!");
    });
}
