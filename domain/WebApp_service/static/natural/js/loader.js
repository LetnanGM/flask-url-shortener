import { app } from "./app/app.js";
import { alertModule } from "./shorturl/utilities/alert.js";
import { validateModule } from "./shorturl/utilities/validator.js";
import { animaModule } from "./shorturl/utilities/anima.js";

app.register("alertModule", alertModule);
app.register("validateModule", validateModule);
app.register("animaModule", animaModule);

const page = document.body.dataset.page;

const routes = {
  landing: () => import("./shorturl/public/landing.js"),
  login: () => import("./shorturl/public/login.js"),
  register: () => import("./shorturl/private/register.js"),
  dashboard: () => import("./shorturl/private/dashboard.js"),
  admin: () => import("./shorturl/private/admin.js"),
};

if (routes[page]) {
  routes[page]().then((mod) => mod.init());
}
