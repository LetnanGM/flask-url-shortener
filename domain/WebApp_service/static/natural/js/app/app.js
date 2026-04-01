/**
 * SnapURL — app.js
 * Handle onclick
 */

class AppHandler {
  constructor() {
    this.modules = {};
    this.events = ["click", "input", "change", "submit"];
    this.init();
  }

  register(name, module) {
    module.state = module.state || {};
    module.app = this;

    this.modules[name] = module;

    if (typeof module.init === "function") {
      module.init();
    }
  }

  init() {
    // Global event delegation
    this.events.forEach((eventType) => {
      document.addEventListener(eventType, (e) => {
        const target = e.target.closest("[data-action]");
        if (!target) return;

        const actionRaw = target.dataset.action;

        let moduleName, action;

        if (actionRaw.includes("#")) {
          [moduleName, action] = actionRaw.split("#");
        } else {
          console.warn("Invalid action format:", actionRaw);
          return;
        }

        const module = this.modules[moduleName];

        if (!module) {
          console.warn(`Module '${moduleName}' not found`);
          return;
        }

        const method = module[action];

        if (typeof method !== "function") {
          console.warn(
            `Action '${action}' not found in module '${moduleName}'`
          );
          return;
        }

        const args = this.extractArgs(target);

        method.call(module, {
          event: e,
          el: target,
          args,
        });
      });
    });

    window.addEventListener("DOMContentLoaded", () => {
      this.scanDirectives();
    });
  }

  extractArgs(el) {
    const args = {};
    for (const key in el.dataset) {
      if (key === "action" || key === "render") continue;
      args[key] = el.dataset[key];
    }
    return args;
  }

  scanDirectives() {
    document.querySelectorAll("[data-render]").forEach((el) => {
      const raw = el.dataset.render;
      const [moduleName, method] = raw.split("#");

      const module = this.modules[moduleName];

      if (!module) {
        console.warn(`Render module '${moduleName}' not found`);
        return;
      }

      if (typeof module[method] !== "function") {
        console.warn(`Render method '${method}' not found`);
        return;
      }

      const args = this.extractArgs(el);

      module[method].call(module, {
        el,
        args,
      });
    });
  }

  get(name_module) {
    if (this.modules) {
      return this.modules[name_module];
    } else {
      alert("Application can't run javascript ES MODULE.");
    }
  }

  clean() {
    this.modules = {};
    return this.modules;
  }
}

export const app = new AppHandler();
