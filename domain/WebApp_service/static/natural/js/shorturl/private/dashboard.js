/**
 * SnapURL — dashboard.js
 * Dashboard page logic: charts, link management, navigation
 */

import { SnapAPI } from "../../api.js";
import { app } from "../../app/app.js";
import { fmtNum } from "../utilities/validator.js";

let _session = null;
let _userLinks = [];
let _charts = {};
let _currentSection = "dashboard";

const anime = app.get("animaModule");
const show = app.get("alertModule");
const val = app.get("validateModule");

/* ══════════════════════════════════════════
   INIT
══════════════════════════════════════════ */
export function init() {
  _session = SnapAPI.auth.requireAuth();
  if (!_session) return;

  // Set up UI
  setupSidebarUser();
  showAdminNav();
  showSection("dashboard");

  // Load data
  loadKPIs();
  loadCharts();
  loadLinks();
}

/* ─── SIDEBAR USER ─── */
function setupSidebarUser() {
  const nameEl = document.getElementById("sidebarName");
  const avatarEl = document.getElementById("sidebarAvatar");
  const roleEl = document.getElementById("sidebarRole");
  const welcomeEl = document.getElementById("welcomeMsg");

  if (nameEl) nameEl.textContent = _session.name;
  if (avatarEl) avatarEl.textContent = _session.name.charAt(0).toUpperCase();
  if (roleEl) roleEl.textContent = _session.role;
  if (welcomeEl)
    welcomeEl.textContent = `Welcome back, ${_session.name.split(" ")[0]}! 👋`;

  // Settings fields
  const setName = document.getElementById("setName");
  const setEmail = document.getElementById("setEmail");
  const setUsername = document.getElementById("setUsername");
  const apiField = document.getElementById("apiKeyField");
  if (setName) setName.value = _session.name;
  if (setEmail) setEmail.value = _session.email;
  if (setUsername) setUsername.value = _session.username;
  if (apiField) apiField.value = _session.apiKey || "sk-snap-not-configured";
}

function showAdminNav() {
  const adminNav = document.getElementById("adminNav");
  if (adminNav && _session && _session.role === "admin")
    adminNav.classList.remove("d-none");
}

/* ── SIDEBAR MOBILE ── */
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");
  if (sb) sb.classList.toggle("open");
  if (overlay) overlay.classList.toggle("d-none");
}

/* ── SECTION SWITCHING ── */
function showSection(name) {
  const sections = ["dashboard", "links", "analytics", "qr", "settings"];
  sections.forEach((s) => {
    const el = document.getElementById(`section-${s}`);
    if (el) el.classList.toggle("d-none", s !== name);
  });

  // Update active nav
  document
    .querySelectorAll(".sidebar-link")
    .forEach((l) => l.classList.remove("active"));
  const activeNav = document.getElementById(`nav-${name}`);
  if (activeNav) activeNav.classList.add("active");

  // Update page title
  const titles = {
    dashboard: "Dashboard",
    links: "My Links",
    analytics: "Analytics",
    qr: "QR Codes",
    settings: "Settings",
  };
  const titleEl = document.getElementById("pageTitle");
  if (titleEl) titleEl.textContent = titles[name] || name;

  _currentSection = name;

  if (name === "analytics" && !_charts.analyticsMain) loadAnalyticsCharts();
  if (name === "qr") renderQRSection();
}

/* ══════════════════════════════════════════
   KPIs
══════════════════════════════════════════ */
function loadKPIs() {
  SnapAPI.analytics.getUserStats(_session.userId).then((res) => {
    if (!res.success) return;
    const s = res.stats;
    anime.animateCount(document.getElementById("kpi-links"), s.totalLinks);
    anime.animateCount(document.getElementById("kpi-clicks"), s.totalClicks);
    anime.animateCount(
      document.getElementById("kpi-visitors"),
      s.totalVisitors
    );
    const ctrEl = document.getElementById("kpi-ctr");
    if (ctrEl) {
      setTimeout(() => {
        ctrEl.textContent = s.ctr;
      }, 800);
    }

    const navBadge = document.getElementById("navLinkCount");
    if (navBadge) navBadge.textContent = s.totalLinks;
  });
}

/* ══════════════════════════════════════════
   CHARTS
══════════════════════════════════════════ */
const CHART_COLORS = {
  accent: "#4f9cf9",
  purple: "#a78bfa",
  green: "#34d399",
  orange: "#fb923c",
  red: "#f87171",
  grid: "rgba(255,255,255,0.05)",
  text: "#8892aa",
};

const chartDefaults = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    x: {
      grid: { color: CHART_COLORS.grid },
      ticks: { color: CHART_COLORS.text, font: { size: 11 } },
    },
    y: {
      grid: { color: CHART_COLORS.grid },
      ticks: { color: CHART_COLORS.text, font: { size: 11 } },
    },
  },
};

function makeGradient(ctx, color) {
  const g = ctx.createLinearGradient(0, 0, 0, 250);
  g.addColorStop(0, color.replace(")", ", 0.3)").replace("rgb", "rgba"));
  g.addColorStop(1, color.replace(")", ", 0)").replace("rgb", "rgba"));
  return g;
}

function loadCharts() {
  SnapAPI.analytics.getChartData("7d").then((res) => {
    if (!res.success) return;
    renderTrafficChart(res);
  });
  SnapAPI.analytics.getDeviceData().then((res) => {
    if (!res.success) return;
    renderDeviceChart(res.data);
  });
  SnapAPI.analytics.getGeoData().then((res) => {
    if (!res.success) return;
    renderGeoList(res.data);
  });
}

function renderTrafficChart(data) {
  const ctx = document.getElementById("trafficChart");
  if (!ctx) return;
  if (_charts.traffic) _charts.traffic.destroy();

  const cCtx = ctx.getContext("2d");
  _charts.traffic = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Clicks",
          data: data.clicks,
          borderColor: CHART_COLORS.accent,
          backgroundColor: makeGradient(cCtx, "rgb(79,156,249)"),
          borderWidth: 2.5,
          pointRadius: 4,
          pointBackgroundColor: CHART_COLORS.accent,
          tension: 0.4,
          fill: true,
        },
        {
          label: "Visitors",
          data: data.visitors,
          borderColor: CHART_COLORS.purple,
          backgroundColor: makeGradient(cCtx, "rgb(167,139,250)"),
          borderWidth: 2.5,
          pointRadius: 4,
          pointBackgroundColor: CHART_COLORS.purple,
          tension: 0.4,
          fill: true,
        },
      ],
    },
    options: {
      ...chartDefaults,
      plugins: {
        legend: {
          display: true,
          labels: {
            color: CHART_COLORS.text,
            usePointStyle: true,
            pointStyleWidth: 8,
            font: { size: 12 },
          },
        },
        tooltip: { mode: "index", intersect: false },
      },
      interaction: { mode: "nearest", axis: "x", intersect: false },
    },
  });
}

function renderDeviceChart(data) {
  const ctx = document.getElementById("deviceChart");
  if (!ctx) return;
  if (_charts.device) _charts.device.destroy();

  _charts.device = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: data.map((d) => d.label),
      datasets: [
        {
          data: data.map((d) => d.value),
          backgroundColor: data.map((d) => d.color),
          borderColor: "#0f1221",
          borderWidth: 3,
        },
      ],
    },
    options: {
      cutout: "70%",
      plugins: { legend: { display: false } },
    },
  });

  // Custom legend
  const legend = document.getElementById("deviceLegend");
  if (legend) {
    legend.innerHTML = data
      .map(
        (d) => `
      <div class="device-legend-item">
        <div class="device-dot" style="background:${d.color}"></div>
        <span style="flex:1">${d.label}</span>
        <strong>${d.value}%</strong>
      </div>
    `
      )
      .join("");
  }
}

function renderGeoList(data) {
  const el = document.getElementById("geoList");
  if (!el) return;
  el.innerHTML = data
    .map(
      (d) => `
    <div class="geo-item">
      <span class="geo-flag">${d.flag}</span>
      <div class="geo-info flex-grow-1">
        <div class="geo-country">${d.country}</div>
        <div class="geo-bar"><div class="geo-bar-fill" style="width:${d.pct}%"></div></div>
      </div>
      <span class="geo-pct">${d.pct}%</span>
    </div>
  `
    )
    .join("");
}

function switchChart(range, btn) {
  document
    .querySelectorAll(".chart-tabs .chart-tab")
    .forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  SnapAPI.analytics.getChartData(range).then((res) => {
    if (res.success) renderTrafficChart(res);
  });
}

function loadTopLinks() {
  const el = document.getElementById("topLinksList");
  if (!el || !_userLinks.length) {
    if (el) el.innerHTML = '<p class="text-muted small">No links yet.</p>';
    return;
  }
  const sorted = [..._userLinks]
    .sort((a, b) => b.clicks - a.clicks)
    .slice(0, 5);
  el.innerHTML = sorted
    .map(
      (l, i) => `
    <div class="top-link-item">
      <span class="top-link-rank">#${i + 1}</span>
      <div class="top-link-info">
        <div class="top-link-alias">snp.ly/${l.alias}</div>
        <div class="top-link-dest">${l.longUrl}</div>
      </div>
      <span class="top-link-clicks">${fmtNum(l.clicks)}</span>
    </div>
  `
    )
    .join("");
}

/* ─── ANALYTICS CHARTS ─── */
function loadAnalyticsCharts() {
  SnapAPI.analytics.getChartData("7d").then((res) => {
    if (!res.success) return;
    const ctx = document.getElementById("analyticsMainChart");
    if (!ctx) return;
    if (_charts.analyticsMain) _charts.analyticsMain.destroy();
    const cCtx = ctx.getContext("2d");
    _charts.analyticsMain = new Chart(ctx, {
      type: "bar",
      data: {
        labels: res.labels,
        datasets: [
          {
            label: "Clicks",
            data: res.clicks,
            backgroundColor: "rgba(79,156,249,0.7)",
            borderRadius: 6,
          },
          {
            label: "Visitors",
            data: res.visitors,
            backgroundColor: "rgba(167,139,250,0.7)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        ...chartDefaults,
        plugins: {
          legend: {
            display: true,
            labels: { color: CHART_COLORS.text, font: { size: 12 } },
          },
        },
      },
    });
  });

  // Browser/OS doughnut charts
  SnapAPI.analytics.getBrowserData().then((res) => {
    const ctx = document.getElementById("browserChart");
    if (!ctx || !res.success) return;
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: res.data.map((d) => d.label),
        datasets: [
          {
            data: res.data.map((d) => d.value),
            backgroundColor: ["#4f9cf9", "#a78bfa", "#34d399", "#fb923c"],
            borderColor: "#0f1221",
            borderWidth: 3,
          },
        ],
      },
      options: {
        cutout: "65%",
        plugins: {
          legend: {
            display: true,
            position: "bottom",
            labels: {
              color: CHART_COLORS.text,
              font: { size: 11 },
              padding: 8,
              boxWidth: 10,
            },
          },
        },
      },
    });
  });
  SnapAPI.analytics.getOsData().then((res) => {
    const ctx = document.getElementById("osChart");
    if (!ctx || !res.success) return;
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: res.data.map((d) => d.label),
        datasets: [
          {
            data: res.data.map((d) => d.value),
            backgroundColor: ["#34d399", "#fb923c", "#4f9cf9", "#a78bfa"],
            borderColor: "#0f1221",
            borderWidth: 3,
          },
        ],
      },
      options: {
        cutout: "65%",
        plugins: {
          legend: {
            display: true,
            position: "bottom",
            labels: {
              color: CHART_COLORS.text,
              font: { size: 11 },
              padding: 8,
              boxWidth: 10,
            },
          },
        },
      },
    });
  });

  SnapAPI.analytics.getReferrers().then((res) => {
    const el = document.getElementById("referrerList");
    if (!el || !res.success) return;
    el.innerHTML = res.data
      .map(
        (r) => `
      <div class="referrer-item">
        <div class="referrer-name flex-grow-1">
          <div>${r.name}</div>
          <div class="referrer-bar"><div class="referrer-bar-fill" style="width:${
            r.pct
          }%"></div></div>
        </div>
        <span class="referrer-count">${fmtNum(r.count)}</span>
      </div>
    `
      )
      .join("");
  });

  // Populate link filter
  const filter = document.getElementById("analyticsLinkFilter");
  if (filter && _userLinks.length) {
    filter.innerHTML =
      '<option value="all">All Links</option>' +
      _userLinks
        .map((l) => `<option value="${l.id}">snp.ly/${l.alias}</option>`)
        .join("");
  }
}

function switchAnalyticsRange(range, btn) {
  document
    .querySelectorAll("#section-analytics .chart-tabs .chart-tab")
    .forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
}
function updateAnalyticsChart() {}

/* ══════════════════════════════════════════
   LINKS
══════════════════════════════════════════ */
function loadLinks() {
  SnapAPI.links.getByUser(_session.userId).then((res) => {
    if (!res.success) return;
    _userLinks = res.links;
    renderLinksTable(_userLinks);
    loadTopLinks();
  });
}

function renderLinksTable(links) {
  const tbody = document.getElementById("linksTableBody");
  const empty = document.getElementById("linksEmpty");
  if (!tbody) return;

  if (!links.length) {
    tbody.innerHTML = "";
    if (empty) empty.classList.remove("d-none");
    return;
  }
  if (empty) empty.classList.add("d-none");

  tbody.innerHTML = links
    .map(
      (l) => `
    <tr>
      <td><a class="link-short" href="#" onclick="copyText('snp.ly/${
        l.alias
      }');return false">snp.ly/${l.alias}</a></td>
      <td><span class="link-dest" title="${l.longUrl}">${l.longUrl}</span></td>
      <td><strong>${fmtNum(l.clicks)}</strong></td>
      <td>${fmtNum(l.visitors)}</td>
      <td><span class="text-muted small">${l.created}</span></td>
      <td><span class="${
        l.status === "active" ? "badge-active" : "badge-inactive"
      }">${l.status}</span></td>
      <td>
        <div class="action-btns">
          <button class="action-btn" title="Copy link" onclick="copyText('snp.ly/${
            l.alias
          }')"><i class="fa-regular fa-copy"></i></button>
          <button class="action-btn" title="View analytics" onclick="showLinkDetail('${
            l.id
          }')"><i class="fa-solid fa-chart-bar"></i></button>
          <button class="action-btn" title="${
            l.status === "active" ? "Deactivate" : "Activate"
          }" onclick="toggleLink('${l.id}')">
            <i class="fa-solid fa-${
              l.status === "active" ? "pause" : "play"
            }"></i>
          </button>
          <button class="action-btn danger" title="Delete" onclick="deleteLink('${
            l.id
          }')"><i class="fa-solid fa-trash"></i></button>
        </div>
      </td>
    </tr>
  `
    )
    .join("");
}

function filterLinks(q) {
  if (!q) {
    renderLinksTable(_userLinks);
    return;
  }
  const f = _userLinks.filter(
    (l) =>
      l.alias.toLowerCase().includes(q.toLowerCase()) ||
      l.longUrl.toLowerCase().includes(q.toLowerCase()) ||
      (l.title || "").toLowerCase().includes(q.toLowerCase())
  );
  renderLinksTable(f);
}

function filterByStatus(status) {
  if (!status) {
    renderLinksTable(_userLinks);
    return;
  }
  renderLinksTable(_userLinks.filter((l) => l.status === status));
}

function sortLinks(by) {
  const sorted = [..._userLinks];
  if (by === "clicks") sorted.sort((a, b) => b.clicks - a.clicks);
  else if (by === "name") sorted.sort((a, b) => a.alias.localeCompare(b.alias));
  else sorted.sort((a, b) => new Date(b.created) - new Date(a.created));
  renderLinksTable(sorted);
}

/* ─── CREATE LINK ─── */
function createLink() {
  const longUrl = document.getElementById("modalLongUrl").value.trim();
  const alias = document.getElementById("modalAlias").value.trim();
  const title = document.getElementById("modalTitle").value.trim();
  const expiry = document.getElementById("modalExpiry").value;

  show.hideAlert("modalAlert");

  if (!longUrl || !isValidUrl(longUrl)) {
    show.showAlert(
      "modalAlert",
      "Please enter a valid URL (include https://)."
    );
    return;
  }

  SnapAPI.links
    .create({ longUrl, alias, title, expiry }, _session.userId)
    .then((res) => {
      if (res.success) {
        bootstrap.Modal.getInstance(
          document.getElementById("shortenModal")
        ).hide();
        show.showToast(`Link created: snp.ly/${res.link.alias}`);
        _userLinks.unshift(res.link);
        renderLinksTable(_userLinks);
        loadKPIs();
        // Clear form
        ["modalLongUrl", "modalAlias", "modalTitle", "modalExpiry"].forEach(
          (id) => {
            const el = document.getElementById(id);
            if (el) el.value = "";
          }
        );
      } else {
        show.showAlert("modalAlert", res.message || "Could not create link.");
      }
    });
}

/* ─── TOGGLE LINK ─── */
function toggleLink(id) {
  SnapAPI.links.toggle(id).then((res) => {
    if (res.success) {
      const link = _userLinks.find((l) => l.id === id);
      if (link) link.status = res.link.status;
      renderLinksTable(_userLinks);
      show.showToast(
        `Link ${res.link.status === "active" ? "activated" : "deactivated"}.`
      );
    }
  });
}

/* ─── DELETE LINK ─── */
function deleteLink(id) {
  if (!confirm("Delete this link? This cannot be undone.")) return;
  SnapAPI.links.delete(id).then((res) => {
    if (res.success) {
      _userLinks = _userLinks.filter((l) => l.id !== id);
      renderLinksTable(_userLinks);
      loadKPIs();
      show.showToast("Link deleted.");
    }
  });
}

/* ─── LINK DETAIL ─── */
function showLinkDetail(id) {
  const link = _userLinks.find((l) => l.id === id);
  if (!link) return;
  const body = document.getElementById("linkDetailBody");
  if (!body) return;

  body.innerHTML = `
    <div class="row g-3 mb-4">
      <div class="col-12">
        <div style="background:var(--bg-hover);border:1px solid var(--border);border-radius:10px;padding:1rem;">
          <div class="d-flex align-items-center gap-3 flex-wrap">
            <div>
              <div class="small text-muted">Short Link</div>
              <div style="font-family:var(--font-head);font-weight:700;color:var(--accent);font-size:1.1rem">snp.ly/${
                link.alias
              }</div>
            </div>
            <div class="flex-grow-1">
              <div class="small text-muted">Destination</div>
              <div class="small" style="word-break:break-all;color:var(--text-secondary)">${
                link.longUrl
              }</div>
            </div>
            <button class="btn btn-copy" onclick="copyText('snp.ly/${
              link.alias
            }')"><i class="fa-regular fa-copy me-1"></i>Copy</button>
          </div>
        </div>
      </div>
    </div>
    <div class="row g-3 mb-4">
      <div class="col-4 text-center">
        <div style="font-family:var(--font-head);font-size:2rem;font-weight:800">${fmtNum(
          link.clicks
        )}</div>
        <div class="small text-muted">Total Clicks</div>
      </div>
      <div class="col-4 text-center">
        <div style="font-family:var(--font-head);font-size:2rem;font-weight:800">${fmtNum(
          link.visitors
        )}</div>
        <div class="small text-muted">Unique Visitors</div>
      </div>
      <div class="col-4 text-center">
        <div style="font-family:var(--font-head);font-size:2rem;font-weight:800">${
          link.clicks ? Math.round((link.visitors / link.clicks) * 100) : 0
        }%</div>
        <div class="small text-muted">Conversion</div>
      </div>
    </div>
    <div style="background:var(--bg-hover);border-radius:10px;padding:1rem;">
      <canvas id="detailChart" height="120"></canvas>
    </div>
  `;

  bootstrap.Modal.getOrCreateInstance(
    document.getElementById("linkDetailModal")
  ).show();

  // Draw mini chart
  setTimeout(() => {
    SnapAPI.analytics.getChartData("7d").then((res) => {
      if (!res.success) return;
      const ctx = document.getElementById("detailChart");
      if (!ctx) return;
      new Chart(ctx, {
        type: "line",
        data: {
          labels: res.labels,
          datasets: [
            {
              label: "Clicks",
              data: res.clicks.map((v) => Math.floor(v * (link.clicks / 1247))),
              borderColor: CHART_COLORS.accent,
              backgroundColor: "rgba(79,156,249,0.1)",
              borderWidth: 2,
              tension: 0.4,
              fill: true,
              pointRadius: 3,
            },
          ],
        },
        options: { ...chartDefaults, plugins: { legend: { display: false } } },
      });
    });
  }, 200);
}

/* ══════════════════════════════════════════
   QR CODES
══════════════════════════════════════════ */
function renderQRSection() {
  const grid = document.getElementById("qrGrid");
  if (!grid) return;
  if (!_userLinks.length) {
    grid.innerHTML =
      '<div class="col-12"><div class="empty-state"><i class="fa-solid fa-qrcode"></i><p>No links yet — create one to generate a QR code.</p></div></div>';
    return;
  }
  grid.innerHTML = _userLinks
    .map(
      (l) => `
    <div class="col-6 col-md-4 col-xl-3">
      <div class="qr-card">
        <div class="qr-canvas-wrap">
          <img src="https://api.qrserver.com/v1/create-qr-code/?size=130x130&data=snp.ly/${
            l.alias
          }&color=0f1221&bgcolor=ffffff" alt="QR" loading="lazy" />
        </div>
        <div class="qr-alias">snp.ly/${l.alias}</div>
        <div class="qr-dest">${l.title || l.longUrl.slice(0, 40) + "…"}</div>
        <a href="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=snp.ly/${
          l.alias
        }" download="qr-${
        l.alias
      }.png" class="btn btn-snap-outline w-100 mt-3" style="font-size:.82rem">
          <i class="fa-solid fa-download me-1"></i>Download PNG
        </a>
      </div>
    </div>
  `
    )
    .join("");
}
