/**
 * SnapURL — admin.js
 * Admin panel: user management, platform stats, platform-wide links
 */

import { SnapAPI } from "../../api.js";
import { app } from "../../app/app.js";
import { fmtNum } from "../utilities/validator.js";

let _allUsers = [];
let _allLinks = [];
let _adminCharts = {};

const anime = app.get("animaModule");
const show = app.get("alertModule");
const val = app.get("validateModule");

export function init() {
  console.log("Admin Page Loaded.");
  const sess = SnapAPI.auth.requireAdmin();
  if (!sess) return;

  // Update sidebar
  const nameEl = document.getElementById("sidebarName");
  const avatarEl = document.getElementById("sidebarAvatar");
  if (nameEl) nameEl.textContent = sess.name;
  if (avatarEl) avatarEl.textContent = sess.name.charAt(0).toUpperCase();

  loadAdminKPIs();
  loadAdminCharts();
  loadAllUsers();
  loadAllLinks();
}

/* ── KPIs ── */
function loadAdminKPIs() {
  SnapAPI.analytics.getPlatformStats().then((res) => {
    if (!res.success) return;
    const s = res.stats;
    anime.animateCount(
      document.getElementById("admin-kpi-users"),
      s.totalUsers
    );
    anime.animateCount(
      document.getElementById("admin-kpi-links"),
      s.totalLinks
    );
    anime.animateCount(
      document.getElementById("admin-kpi-clicks"),
      s.totalClicks
    );
  });
}

/* ── CHARTS ── */
function loadAdminCharts() {
  SnapAPI.analytics.getChartData("30d").then((res) => {
    if (!res.success) return;
    const ctx = document.getElementById("adminGrowthChart");
    if (!ctx) return;

    const cCtx = ctx.getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: res.labels,
        datasets: [
          {
            label: "Total Clicks",
            data: res.clicks.map((v) => v * 8),
            borderColor: "#4f9cf9",
            backgroundColor: "rgba(79,156,249,0.08)",
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointRadius: 2,
          },
          {
            label: "New Links",
            data: res.visitors.map((v) => Math.floor(v / 3)),
            borderColor: "#34d399",
            backgroundColor: "rgba(52,211,153,0.05)",
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
            labels: {
              color: "#8892aa",
              font: { size: 12 },
              usePointStyle: true,
            },
          },
          tooltip: { mode: "index", intersect: false },
        },
        scales: {
          x: {
            grid: { color: "rgba(255,255,255,0.05)" },
            ticks: { color: "#8892aa", font: { size: 10 }, maxTicksLimit: 8 },
          },
          y: {
            grid: { color: "rgba(255,255,255,0.05)" },
            ticks: { color: "#8892aa", font: { size: 11 } },
          },
        },
      },
    });
  });

  // Role chart
  SnapAPI.users.getAll().then((res) => {
    if (!res.success) return;
    const adminCount = res.users.filter((u) => u.role === "admin").length;
    const userCount = res.users.filter((u) => u.role === "user").length;
    const ctx = document.getElementById("adminRoleChart");
    if (!ctx) return;

    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Users", "Admins"],
        datasets: [
          {
            data: [userCount, adminCount],
            backgroundColor: ["#4f9cf9", "#f87171"],
            borderColor: "#0f1221",
            borderWidth: 3,
          },
        ],
      },
      options: {
        cutout: "70%",
        plugins: {
          legend: {
            display: true,
            position: "bottom",
            labels: {
              color: "#8892aa",
              font: { size: 12 },
              padding: 12,
              boxWidth: 10,
            },
          },
        },
      },
    });
  });
}

/* ── USERS TABLE ── */
function loadAllUsers() {
  SnapAPI.users.getAll().then((res) => {
    if (!res.success) return;
    _allUsers = res.users;
    renderAdminUsersTable(_allUsers);
  });
}

function renderAdminUsersTable(users) {
  const tbody = document.getElementById("adminUsersTable");
  if (!tbody) return;

  const allLinks = _allLinks.length ? _allLinks : [];

  tbody.innerHTML = users
    .map((u) => {
      const userLinks = allLinks.filter((l) => l.userId === u.id);
      const userClicks = userLinks.reduce((a, l) => a + l.clicks, 0);
      return `
      <tr>
        <td>
          <div class="d-flex align-items-center gap-2">
            <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#a78bfa);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0">${u.name.charAt(
              0
            )}</div>
            <div>
              <div style="font-weight:600;font-size:.88rem">${u.name}</div>
              <div style="font-size:.75rem;color:var(--text-muted)">@${
                u.username
              }</div>
            </div>
          </div>
        </td>
        <td><span class="text-muted small">${u.email}</span></td>
        <td><span class="${
          u.role === "admin" ? "badge-admin" : "badge-user"
        }">${u.role}</span></td>
        <td>${userLinks.length}</td>
        <td>${fmtNum(userClicks)}</td>
        <td><span class="text-muted small">${u.joined}</span></td>
        <td><span class="${
          u.status === "active" ? "badge-active" : "badge-inactive"
        }">${u.status}</span></td>
        <td>
          <div class="action-btns">
            <button class="action-btn" title="${
              u.status === "active" ? "Deactivate" : "Activate"
            }" onclick="toggleUser('${u.id}')">
              <i class="fa-solid fa-${
                u.status === "active" ? "ban" : "check"
              }"></i>
            </button>
            <button class="action-btn danger" title="Delete user" onclick="deleteUser('${
              u.id
            }')">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </td>
      </tr>
    `;
    })
    .join("");
}

function filterAdminUsers(q) {
  if (!q) {
    renderAdminUsersTable(_allUsers);
    return;
  }
  const f = _allUsers.filter(
    (u) =>
      u.name.toLowerCase().includes(q.toLowerCase()) ||
      u.email.toLowerCase().includes(q.toLowerCase()) ||
      u.username.toLowerCase().includes(q.toLowerCase())
  );
  renderAdminUsersTable(f);
}

function toggleUser(id) {
  SnapAPI.users.toggleStatus(id).then((res) => {
    if (res.success) {
      loadAllUsers();
      show.showToast("User status updated.");
    }
  });
}

function deleteUser(id) {
  if (!confirm("Delete this user and all their data?")) return;
  SnapAPI.users.delete(id).then((res) => {
    if (res.success) {
      _allUsers = _allUsers.filter((u) => u.id !== id);
      renderAdminUsersTable(_allUsers);
      show.showToast("User deleted.");
      loadAdminKPIs();
    }
  });
}

function addUser() {
  const name = document.getElementById("addUserName").value.trim();
  const email = document.getElementById("addUserEmail").value.trim();
  const password = document.getElementById("addUserPw").value;
  const role = document.getElementById("addUserRole").value;
  if (!name || !email || !password) {
    show.showToast("Please fill all fields.", "error");
    return;
  }
  SnapAPI.users
    .create({ name, email, username: email.split("@")[0], password, role })
    .then((res) => {
      if (res.success) {
        bootstrap.Modal.getInstance(
          document.getElementById("addUserModal")
        ).hide();
        show.showToast("User created successfully.");
        loadAllUsers();
        loadAdminKPIs();
      }
    });
}

/* ── LINKS TABLE ── */
function loadAllLinks() {
  SnapAPI.links.getAll().then((res) => {
    if (!res.success) return;
    _allLinks = res.links;
    renderAdminLinksTable(_allLinks);
    // re-render users table with link counts
    if (_allUsers.length) renderAdminUsersTable(_allUsers);
  });
}

function renderAdminLinksTable(links) {
  const tbody = document.getElementById("adminLinksTable");
  if (!tbody) return;

  tbody.innerHTML = links
    .map(
      (l) => `
    <tr>
      <td><span class="link-short">snp.ly/${l.alias}</span></td>
      <td><span class="text-muted small">${l.userId}</span></td>
      <td><span class="link-dest" style="max-width:200px" title="${
        l.longUrl
      }">${l.longUrl}</span></td>
      <td><strong>${fmtNum(l.clicks)}</strong></td>
      <td><span class="text-muted small">${l.created}</span></td>
      <td><span class="${
        l.status === "active" ? "badge-active" : "badge-inactive"
      }">${l.status}</span></td>
      <td>
        <div class="action-btns">
          <button class="action-btn" onclick="copyText('snp.ly/${
            l.alias
          }')"><i class="fa-regular fa-copy"></i></button>
          <button class="action-btn danger" onclick="adminDeleteLink('${
            l.id
          }')"><i class="fa-solid fa-trash"></i></button>
        </div>
      </td>
    </tr>
  `
    )
    .join("");
}

function filterAdminLinks(q) {
  if (!q) {
    renderAdminLinksTable(_allLinks);
    return;
  }
  const f = _allLinks.filter(
    (l) =>
      l.alias.toLowerCase().includes(q.toLowerCase()) ||
      l.longUrl.toLowerCase().includes(q.toLowerCase())
  );
  renderAdminLinksTable(f);
}

function adminDeleteLink(id) {
  if (!confirm("Delete this link permanently?")) return;
  SnapAPI.links.delete(id).then((res) => {
    if (res.success) {
      _allLinks = _allLinks.filter((l) => l.id !== id);
      renderAdminLinksTable(_allLinks);
      show.showToast("Link deleted.");
    }
  });
}
