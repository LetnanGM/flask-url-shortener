/* ─── NUMBER FORMAT ─── */
export function fmtNum(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1) + "M";
  if (n >= 1000) return (n / 1000).toFixed(1) + "K";
  return n.toString();
}

/* ─── VALIDATE URL ─── */
export function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

export const validateModule = {
  /* ─── TOGGLE PASSWORD ─── */
  togglePassword(e) {
    const id = e.args.id;
    const btn_id = e.args.btn;

    const input = document.getElementById(id);
    const btn = document.getElementById(btn_id);
    if (!input) return;
    if (input.type === "password") {
      input.type = "text";
      btn.innerHTML = '<i class="fa-regular fa-eye-slash"></i>';
    } else {
      input.type = "password";
      btn.innerHTML = '<i class="fa-regular fa-eye"></i>';
    }
  },

  /* ─── PASSWORD STRENGTH ─── */
  checkPasswordStrength(e) {
    const pw = document.getElementById(e.args.pw).value.trim();
    const bar = document.getElementById("pwBar");
    const label = document.getElementById("pwLabel");
    if (!bar || !label) return;
    let score = 0;
    if (pw.length >= 8) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    const levels = [
      { w: "25%", bg: "#f87171", text: "Weak" },
      { w: "50%", bg: "#fb923c", text: "Fair" },
      { w: "75%", bg: "#fbbf24", text: "Good" },
      { w: "100%", bg: "#34d399", text: "Strong" },
    ];
    const l = levels[score - 1] || { w: "0%", bg: "transparent", text: "" };
    bar.style.width = l.w;
    bar.style.background = l.bg;
    label.textContent = l.text;
    label.style.color = l.bg;
  },
};
