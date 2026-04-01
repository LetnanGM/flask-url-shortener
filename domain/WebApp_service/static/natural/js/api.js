/**
 * SnapURL — API Layer (api.js)
 * ─────────────────────────────────────────────────
 * This file acts as the bridge between the frontend and backend.
 * For demo/dev: uses localStorage as a mock database.
 * For production (Flask/Django/Node): swap each method to a real fetch() call.
 *
 * Flask integration guide:
 *   const API_BASE = 'http://localhost:5000/api';  // point to your Flask server
 *   Then replace mock* methods with:  return fetch(`${API_BASE}/endpoint`, {...}).then(r=>r.json());
 */

export const SnapAPI = (() => {
  const API_BASE = "/api"; // Set to Flask base URL e.g. 'http://localhost:5000/api'
  const USE_MOCK = false; // Toggle false to use real API

  /* ─── MOCK DATA STORE ─── */
  const DB = {
    get(k, def) {
      try {
        const v = localStorage.getItem("snap_" + k);
        return v ? JSON.parse(v) : def;
      } catch {
        return def;
      }
    },
    set(k, v) {
      try {
        localStorage.setItem("snap_" + k, JSON.stringify(v));
      } catch {}
    },
  };

  /* ─── SEED INITIAL DATA ─── */
  function seedIfEmpty() {
    if (DB.get("seeded", false)) return;
    const users = [
      {
        id: "u1",
        name: "Admin User",
        email: "admin@snapurl.io",
        username: "admin",
        password: "admin123",
        role: "admin",
        status: "active",
        joined: "2024-01-15",
        apiKey: "sk-snap-admin-abc123",
      },
      {
        id: "u2",
        name: "John Doe",
        email: "user@snapurl.io",
        username: "johndoe",
        password: "user123",
        role: "user",
        status: "active",
        joined: "2024-03-22",
        apiKey: "sk-snap-user-xyz789",
      },
      {
        id: "u3",
        name: "Alice Smith",
        email: "alice@example.com",
        username: "alice",
        password: "alice123",
        role: "user",
        status: "active",
        joined: "2024-05-10",
        apiKey: "sk-snap-alice-def456",
      },
      {
        id: "u4",
        name: "Bob Johnson",
        email: "bob@example.com",
        username: "bobjohnson",
        password: "bob123",
        role: "user",
        status: "inactive",
        joined: "2024-06-30",
        apiKey: "sk-snap-bob-ghi012",
      },
    ];
    const links = [
      {
        id: "l1",
        userId: "u2",
        shortCode: "promo24",
        alias: "promo24",
        title: "Product Launch 2024",
        longUrl:
          "https://example.com/big/product/launch/campaign/2024?utm_source=snapurl&utm_medium=social",
        clicks: 1247,
        visitors: 983,
        created: "2024-11-01",
        status: "active",
        expiry: null,
      },
      {
        id: "l2",
        userId: "u2",
        shortCode: "docs",
        alias: "docs",
        title: "Documentation Site",
        longUrl:
          "https://docs.mycompany.com/getting-started/installation/v2/en",
        clicks: 562,
        visitors: 441,
        created: "2024-11-15",
        status: "active",
        expiry: null,
      },
      {
        id: "l3",
        userId: "u2",
        shortCode: "meet23",
        alias: "meet23",
        title: "Team Meeting Link",
        longUrl: "https://meet.google.com/xyz-abcd-efg?authuser=0",
        clicks: 88,
        visitors: 72,
        created: "2024-12-01",
        status: "inactive",
        expiry: "2025-12-31",
      },
      {
        id: "l4",
        userId: "u3",
        shortCode: "alice-blog",
        alias: "alice-blog",
        title: "My Tech Blog",
        longUrl: "https://alicewrites.dev/posts/why-i-love-open-source-2024",
        clicks: 340,
        visitors: 290,
        created: "2024-10-20",
        status: "active",
        expiry: null,
      },
      {
        id: "l5",
        userId: "u1",
        shortCode: "admin-ref",
        alias: "admin-ref",
        title: "Admin Reference Doc",
        longUrl: "https://internal.company.com/admin/reference/2024",
        clicks: 45,
        visitors: 38,
        created: "2024-09-05",
        status: "active",
        expiry: null,
      },
    ];
    DB.set("users", users);
    DB.set("links", links);
    DB.set("platform", {
      totalLinks: 18472,
      totalUsers: 3291,
      totalClicks: 941203,
      totalCountries: 87,
    });
    DB.set("seeded", true);
  }

  seedIfEmpty();

  /* ─── AUTH ─── */
  const auth = {
    login(email, password) {
      if (USE_MOCK) {
        const users = DB.get("users", []);
        const user = users.find(
          (u) => u.email === email && u.password === password
        );
        if (!user)
          return Promise.resolve({
            success: false,
            message: "Invalid email or password.",
          });
        const session = {
          userId: user.id,
          name: user.name,
          email: user.email,
          username: user.username,
          role: user.role,
          apiKey: user.apiKey,
        };
        sessionStorage.setItem("snap_session", JSON.stringify(session));
        return Promise.resolve({ success: true, user: session });
      }
      return fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      }).then((r) => r.json());
    },

    register(data) {
      if (USE_MOCK) {
        const users = DB.get("users", []);
        if (users.find((u) => u.email === data.email))
          return Promise.resolve({
            success: false,
            message: "Email already registered.",
          });
        if (users.find((u) => u.username === data.username))
          return Promise.resolve({
            success: false,
            message: "Username already taken.",
          });
        const newUser = {
          id: "u" + Date.now(),
          ...data,
          role: "user",
          status: "active",
          joined: new Date().toISOString().slice(0, 10),
          apiKey: "sk-snap-" + Math.random().toString(36).slice(2, 18),
        };
        users.push(newUser);
        DB.set("users", users);
        return Promise.resolve({
          success: true,
          message: "Account created! Please log in.",
        });
      }

      return fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json());
    },

    logout() {
      sessionStorage.removeItem("snap_session");
      return Promise.resolve({ success: true });
    },

    getSession() {
      try {
        return JSON.parse(sessionStorage.getItem("snap_session"));
      } catch {
        return null;
      }
    },

    requireAuth(redirect = "login.html") {
      const s = this.getSession();
      if (!s) {
        window.location.href = redirect;
        return null;
      }
      return s;
    },

    requireAdmin() {
      const s = this.requireAuth();
      if (s && s.role !== "admin") {
        window.location.href = "/vebya_theorem";
        return null;
      }
      return s;
    },
  };

  /* ─── LINKS ─── */
  const links = {
    getByUser(userId) {
      if (USE_MOCK) {
        const all = DB.get("links", []);
        return Promise.resolve({
          success: true,
          links: all.filter((l) => l.userId === userId),
        });
      }
      return fetch(`${API_BASE}/links?userId=${userId}`, {
        headers: _authHeaders(),
      }).then((r) => r.json());
    },

    getAll() {
      if (USE_MOCK)
        return Promise.resolve({ success: true, links: DB.get("links", []) });
      return fetch(`${API_BASE}/links/all`, { headers: _authHeaders() }).then(
        (r) => r.json()
      );
    },

    create(data, userId) {
      if (USE_MOCK) {
        const all = DB.get("links", []);
        const alias = data.alias || Math.random().toString(36).slice(2, 8);
        if (all.find((l) => l.alias === alias))
          return Promise.resolve({
            success: false,
            message: "Alias already in use.",
          });
        const newLink = {
          id: "l" + Date.now(),
          userId,
          shortCode: alias,
          alias,
          title: data.title || alias,
          longUrl: data.longUrl,
          clicks: 0,
          visitors: 0,
          created: new Date().toISOString().slice(0, 10),
          status: "active",
          expiry: data.expiry || null,
        };
        all.push(newLink);
        DB.set("links", all);
        // bump platform stats
        const p = DB.get("platform", {});
        p.totalLinks = (p.totalLinks || 0) + 1;
        DB.set("platform", p);
        return Promise.resolve({ success: true, link: newLink });
      }

      return fetch(`${API_BASE}/links`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ..._authHeaders() },
        body: JSON.stringify({ ...data, userId }),
      }).then((r) => r.json());
    },

    createPublic(longUrl) {
      if (USE_MOCK) {
        const alias = Math.random().toString(36).slice(2, 8);
        const p = DB.get("platform", {});
        p.totalLinks = (p.totalLinks || 0) + 1;
        DB.set("platform", p);
        return Promise.resolve({
          status: true,
          link: { alias, shortUrl: `snp.ly/${alias}`, longUrl },
        });
      }

      return fetch(`${API_BASE}/links/public`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ longuri: longUrl }),
      }).then((r) => r.json());
    },

    toggle(id) {
      if (USE_MOCK) {
        const all = DB.get("links", []);
        const link = all.find((l) => l.id === id);
        if (!link) return Promise.resolve({ success: false });
        link.status = link.status === "active" ? "inactive" : "active";
        DB.set("links", all);
        return Promise.resolve({ status: true, link });
      }
      return fetch(`${API_BASE}/links/${id}/toggle`, {
        method: "PATCH",
        headers: _authHeaders(),
      }).then((r) => r.json());
    },

    delete(id) {
      if (USE_MOCK) {
        let all = DB.get("links", []);
        all = all.filter((l) => l.id !== id);
        DB.set("links", all);
        return Promise.resolve({ success: true });
      }
      return fetch(`${API_BASE}/links/${id}`, {
        method: "DELETE",
        headers: _authHeaders(),
      }).then((r) => r.json());
    },
  };

  /* ─── ANALYTICS ─── */
  const analytics = {
    getPlatformStats() {
      if (USE_MOCK)
        return Promise.resolve({
          success: true,
          stats: DB.get("platform", {
            totalLinks: 0,
            totalUsers: 0,
            totalClicks: 0,
            totalCountries: 0,
          }),
        });
      return fetch(`${API_BASE}/analytics/platform`).then((r) => r.json());
    },

    getUserStats(userId) {
      if (USE_MOCK) {
        const userLinks = DB.get("links", []).filter(
          (l) => l.userId === userId
        );
        const totalClicks = userLinks.reduce((a, l) => a + l.clicks, 0);
        const totalVisitors = userLinks.reduce((a, l) => a + l.visitors, 0);
        return Promise.resolve({
          success: true,
          stats: {
            totalLinks: userLinks.length,
            totalClicks,
            totalVisitors,
            ctr: userLinks.length
              ? Math.round((totalClicks / (totalVisitors || 1)) * 100 * 10) /
                  10 +
                "%"
              : "0%",
          },
        });
      }
      return fetch(`${API_BASE}/analytics/user/${userId}`, {
        headers: _authHeaders(),
      }).then((r) => r.json());
    },

    getChartData(range = "7d") {
      // Generate mock time-series data
      const days = range === "7d" ? 7 : range === "30d" ? 30 : 90;
      const labels = [];
      const clicks = [];
      const visitors = [];
      for (let i = days - 1; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        labels.push(
          days <= 7
            ? d.toLocaleDateString("en", { weekday: "short" })
            : d.toLocaleDateString("en", { month: "short", day: "numeric" })
        );
        const base = Math.floor(Math.random() * 80) + 20;
        clicks.push(base + Math.floor(Math.random() * 40));
        visitors.push(Math.floor(base * 0.7 + Math.random() * 20));
      }
      return Promise.resolve({ success: true, labels, clicks, visitors });
    },

    getDeviceData() {
      return Promise.resolve({
        success: true,
        data: [
          { label: "Mobile", value: 54, color: "#4f9cf9" },
          { label: "Desktop", value: 33, color: "#a78bfa" },
          { label: "Tablet", value: 13, color: "#34d399" },
        ],
      });
    },

    getBrowserData() {
      return Promise.resolve({
        success: true,
        data: [
          { label: "Chrome", value: 48 },
          { label: "Safari", value: 28 },
          { label: "Firefox", value: 12 },
          { label: "Edge", value: 12 },
        ],
      });
    },

    getOsData() {
      return Promise.resolve({
        success: true,
        data: [
          { label: "Android", value: 38 },
          { label: "iOS", value: 26 },
          { label: "Windows", value: 24 },
          { label: "macOS", value: 12 },
        ],
      });
    },

    getGeoData() {
      return Promise.resolve({
        success: true,
        data: [
          { country: "United States", flag: "🇺🇸", pct: 32 },
          { country: "Indonesia", flag: "🇮🇩", pct: 18 },
          { country: "India", flag: "🇮🇳", pct: 14 },
          { country: "United Kingdom", flag: "🇬🇧", pct: 9 },
          { country: "Germany", flag: "🇩🇪", pct: 7 },
        ],
      });
    },

    getReferrers() {
      return Promise.resolve({
        success: true,
        data: [
          { name: "Twitter / X", count: 421, pct: 35 },
          { name: "Direct", count: 380, pct: 31 },
          { name: "Google Search", count: 210, pct: 17 },
          { name: "WhatsApp", count: 120, pct: 10 },
          { name: "Others", count: 87, pct: 7 },
        ],
      });
    },
  };

  /* ─── USERS (Admin) ─── */
  const users = {
    getAll() {
      if (USE_MOCK)
        return Promise.resolve({ success: true, users: DB.get("users", []) });
      return fetch(`${API_BASE}/users`, { headers: _authHeaders() }).then((r) =>
        r.json()
      );
    },

    create(data) {
      if (USE_MOCK) {
        const all = DB.get("users", []);
        const newUser = {
          id: "u" + Date.now(),
          ...data,
          status: "active",
          joined: new Date().toISOString().slice(0, 10),
          apiKey: "sk-snap-" + Math.random().toString(36).slice(2, 18),
        };
        all.push(newUser);
        DB.set("users", all);
        const p = DB.get("platform", {});
        p.totalUsers = (p.totalUsers || 0) + 1;
        DB.set("platform", p);
        return Promise.resolve({ success: true, user: newUser });
      }
      return fetch(`${API_BASE}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ..._authHeaders() },
        body: JSON.stringify(data),
      }).then((r) => r.json());
    },

    toggleStatus(id) {
      if (USE_MOCK) {
        const all = DB.get("users", []);
        const u = all.find((u) => u.id === id);
        if (u) {
          u.status = u.status === "active" ? "inactive" : "active";
          DB.set("users", all);
        }
        return Promise.resolve({ success: true });
      }
      return fetch(`${API_BASE}/users/${id}/toggle`, {
        method: "PATCH",
        headers: _authHeaders(),
      }).then((r) => r.json());
    },

    delete(id) {
      if (USE_MOCK) {
        DB.set(
          "users",
          DB.get("users", []).filter((u) => u.id !== id)
        );
        return Promise.resolve({ success: true });
      }
      return fetch(`${API_BASE}/users/${id}`, {
        method: "DELETE",
        headers: _authHeaders(),
      }).then((r) => r.json());
    },

    updateProfile(id, data) {
      if (USE_MOCK) {
        const all = DB.get("users", []);
        const u = all.find((u) => u.id === id);
        if (u) {
          Object.assign(u, data);
          DB.set("users", all);
        }
        const sess = JSON.parse(sessionStorage.getItem("snap_session") || "{}");
        Object.assign(sess, data);
        sessionStorage.setItem("snap_session", JSON.stringify(sess));
        return Promise.resolve({ success: true });
      }
      return fetch(`${API_BASE}/users/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ..._authHeaders() },
        body: JSON.stringify(data),
      }).then((r) => r.json());
    },
  };

  /* ─── HELPERS ─── */
  function _authHeaders() {
    const s = auth.getSession();
    return s ? { Authorization: `Bearer ${s.apiKey}` } : {};
  }

  /* ─── LIVE TICKER DATA ─── */
  const tickerMessages = [
    "Someone in Jakarta shortened a link just now",
    "A link from New York got 12 clicks in the last minute",
    "New user registered from Berlin",
    "A campaign link hit 1,000 clicks milestone",
    "Someone in London created a custom alias",
    "A QR code was downloaded from Sydney",
    "New API key generated from Singapore",
    "Traffic spike detected on a marketing link",
    "A link from Mumbai got shared on WhatsApp",
    "Someone in Toronto created their 10th link",
  ];

  function getTickerMessage() {
    return tickerMessages[Math.floor(Math.random() * tickerMessages.length)];
  }

  return { auth, links, analytics, users, getTickerMessage };
})();

/**
 * Flask Integration Reference
 * ─────────────────────────────────────────────
 * Backend routes your Flask app should implement:
 *
 * POST   /api/auth/login          → {email, password} → {success, user}
 * POST   /api/auth/register       → {name, email, username, password} → {success, message}
 *
 * GET    /api/links?userId=       → {success, links}
 * GET    /api/links/all           → {success, links}  (admin)
 * POST   /api/links               → {longUrl, alias?, title?, expiry?} → {success, link}
 * POST   /api/links/public        → {longUrl} → {success, link}
 * PATCH  /api/links/:id/toggle    → {success, link}
 * DELETE /api/links/:id           → {success}
 *
 * GET    /api/analytics/platform  → {success, stats}
 * GET    /api/analytics/user/:id  → {success, stats}
 *
 * GET    /api/users               → {success, users}  (admin)
 * POST   /api/users               → {success, user}   (admin)
 * PATCH  /api/users/:id/toggle    → {success}         (admin)
 * DELETE /api/users/:id           → {success}         (admin)
 * PATCH  /api/users/:id           → {success}
 *
 * GET    /:shortCode              → redirect to original URL (Flask handles this)
 */
