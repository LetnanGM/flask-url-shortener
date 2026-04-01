import { SnapAPI } from "../../api.js";
import { app } from "../../app/app.js";
import { fmtNum } from "../utilities/validator.js";

/* ══════════════════════════════════════════
   AUTH PAGES
══════════════════════════════════════════ */

export const AuthModule = {
  /* ─── LOGIN ─── */
  handleLogin(e) {
    const alert = app.get("alertModule");
    const anime = app.get("animaModule");

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;
    alert.hideAlert("loginAlert");
    anime.setButtonLoading("loginBtn", true);

    SnapAPI.auth.login(email, password).then((res) => {
      anime.setButtonLoading("loginBtn", false);
      if (res.success) {
        alert.showToast("Welcome back, " + res.user.name.split(" ")[0] + "!");
        setTimeout(() => {
          window.location.href = "dashboard.html";
        }, 600);
      } else {
        alert.showAlert("loginAlert", res.message || "Login failed.");
      }
    });
  },

  /* ─── SOCIAL LOGIN ─── */
  socialLogin(provider) {
    const alert = app.get("alertModule");

    alert.showToast(
      `${
        provider.charAt(0).toUpperCase() + provider.slice(1)
      } OAuth not configured in demo mode.`,
      "error"
    );
  },

  /* ─── LOGOUT ─── */
  handleLogout() {
    const alert = app.get("alertModule");

    SnapAPI.auth.logout().then(() => {
      alert.showToast("Signed out successfully.");
      setTimeout(() => {
        window.location.href = "login.html";
      }, 600);
    });
  },

  /* ─── COPY API KEY ─── */
  copyApiKey() {
    const el = document.getElementById("apiKeyField");
    if (el) copyText(el.value);
  },

  /* ─── PROFILE SAVE ─── */
  saveProfile() {
    const alert = app.get("alertModule");

    const sess = SnapAPI.auth.getSession();
    if (!sess) return;
    const name = document.getElementById("setName").value.trim();
    const email = document.getElementById("setEmail").value.trim();
    const username = document.getElementById("setUsername").value.trim();
    SnapAPI.users
      .updateProfile(sess.userId, { name, email, username })
      .then((res) => {
        if (res.success) {
          alert.showAlert(
            "settingsAlert",
            "Profile updated successfully.",
            "success"
          );
          document.getElementById("sidebarName").textContent = name;
          document.getElementById("sidebarAvatar").textContent = name
            .charAt(0)
            .toUpperCase();
        }
      });
  },

  changePassword() {
    const alert = app.get("alertModule");
    alert.showToast("Password change requires backend integration.", "error");
  },
};

export function init() {
  console.log("Login Module Loaded.");
  // If already logged in, redirect
  app.register("AuthModule", AuthModule);
  const sess = SnapAPI.auth.getSession();
  if (sess) window.location.href = "/dashboard";

  // Load left panel stat
  SnapAPI.analytics.getPlatformStats().then((res) => {
    if (res.success) {
      const el = document.getElementById("left-stat-links");
      if (el) el.textContent = fmtNum(Math.floor(res.stats.totalLinks / 30));
    }
  });

  document.getElementById("loginForm").addEventListener("submit", (e) => {
    e.preventDefault();
    AuthModule.handleLogin(e);
  });
}
