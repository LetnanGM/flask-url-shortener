import { SnapAPI } from "../../api.js";
import { app } from "../../app/app.js";

export const RegisterModule = {
  /* ─── REGISTER ─── */
  handleRegister(e) {
    const alert = app.get("alertModule");
    const anime = app.get("animaModule");

    const firstName = document.getElementById("regFirstName").value.trim();
    const lastName = document.getElementById("regLastName").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const username = document.getElementById("regUsername").value.trim();
    const password = document.getElementById("regPassword").value;
    const confirm = document.getElementById("regConfirm").value;

    alert.hideAlert("registerAlert");

    if (password !== confirm) {
      alert.showAlert("registerAlert", "Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      alert.showAlert(
        "registerAlert",
        "Password must be at least 8 characters."
      );
      return;
    }

    anime.setButtonLoading("registerBtn", true);

    SnapAPI.auth
      .register({
        name: firstName + " " + lastName,
        email: email,
        username: username,
        password: password,
      })
      .then((res) => {
        anime.setButtonLoading("registerBtn", false);
        if (res.status) {
          alert.showAlert(
            "registerAlert",
            "Account created! Redirecting to login…",
            "success"
          );
          setTimeout(() => {
            window.location.href = "/login";
          }, 1500);
        } else {
          alert.showAlert(
            "registerAlert",
            res.reason || "Registration failed."
          );
        }
      });
  },
};

export function init() {
  console.log("Register Module Loaded.");
  app.register("RegisterMoudle", RegisterModule);

  document.getElementById("registerForm").addEventListener("submit", (e) => {
    e.preventDefault();
    RegisterModule.handleRegister(e);
  });
}
