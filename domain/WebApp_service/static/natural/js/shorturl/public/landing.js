import { SnapAPI } from "../../api.js";
import { app } from "../../app/app.js";
import { copyText } from "../utilities/alert.js";
import { isValidUrl } from "../utilities/validator.js";

export const landModule = {
  initLandingPage() {
    // Animate hero user count
    const anime = app.get("animaModule");
    SnapAPI.analytics.getPlatformStats().then((res) => {
      if (!res.status) return;
      const s = res.stats;
      const heroEl = document.getElementById("hero-users");
      if (heroEl) anime.animateCount(heroEl, s.totalUsers);

      // Stat counters
      setTimeout(() => {
        anime.animateCount(document.getElementById("stat-links"), s.totalLinks);
        anime.animateCount(document.getElementById("stat-users"), s.totalUsers);
        anime.animateCount(
          document.getElementById("stat-clicks"),
          s.totalClicks
        );
        anime.animateCount(
          document.getElementById("stat-countries"),
          s.totalCountries
        );
      }, 400);
    });

    // Live ticker
    const ticker = document.getElementById("tickerTrack");
    if (ticker) {
      let msg = SnapAPI.getTickerMessage();
      ticker.textContent = msg;
      setInterval(() => {
        ticker.style.opacity = "0";
        setTimeout(() => {
          ticker.textContent = SnapAPI.getTickerMessage();
          ticker.style.opacity = "1";
          ticker.style.transition = "opacity .5s";
        }, 400);
      }, 4000);
    }

    // If already logged in show dashboard link
    const sess = SnapAPI.auth.getSession();
    if (sess) {
      const btn = document.querySelector(
        '.btn-snap-primary[href="{{ register_url }}"]'
      );
      if (btn) {
        btn.href = "{{ dashboard_url }}";
        btn.innerHTML =
          '<i class="fa-solid fa-gauge-high me-2"></i>My Dashboard';
      }
    }
  },

  /* ─── SHORTEN (Public) ─── */
  handleShorten() {
    const input = document.getElementById("longUrl");
    const url = input ? input.value.trim() : "";
    const resultBox = document.getElementById("resultBox");
    const errorBox = document.getElementById("errorBox");
    const btn = document.getElementById("shortenBtn");

    if (errorBox) errorBox.classList.add("d-none");
    if (resultBox) resultBox.classList.add("d-none");

    if (!url) {
      if (errorBox) {
        errorBox.textContent = "Please enter a URL.";
        errorBox.classList.remove("d-none");
      }
      return;
    }
    if (!isValidUrl(url)) {
      if (errorBox) {
        errorBox.textContent =
          "That doesn't look like a valid URL. Include https://";
        errorBox.classList.remove("d-none");
      }
      return;
    }

    if (btn) {
      btn.disabled = true;
      btn.innerHTML =
        '<i class="fa-solid fa-spinner fa-spin me-2"></i>Shortening…';
    }

    SnapAPI.links.createPublic(url).then((res) => {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-scissors me-2"></i>Shorten';
      }
      let shortUrl = `${window.location.protocol}//${document.domain}/${res.data.alias}`;

      if (res.status) {
        const display = document.getElementById("shortLinkDisplay");
        if (display) {
          display.textContent = shortUrl;
          display.href = res.data.longUrl;
        }
        if (resultBox) resultBox.classList.remove("d-none");
        window._lastShortLink = shortUrl;
      } else {
        if (errorBox) {
          errorBox.textContent = res.reason || "Something went wrong.";
          errorBox.classList.remove("d-none");
        }
      }
    });
  },

  copyShortLink() {
    if (window._lastShortLink) copyText(window._lastShortLink);
  },
};

export function init() {
  console.log("LandingPage Module loaded.");
  app.register("landModule", landModule);
  landModule.initLandingPage();

  // Enter key on URL input
  document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("longUrl");
    if (input)
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") landModule.handleShorten();
      });
  });
}
