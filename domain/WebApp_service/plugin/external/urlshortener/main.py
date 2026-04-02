from flask import Flask, request, jsonify, render_template, redirect, flash
from application.bootstrap import init_shortener


class apiServiceShortener:
    def __init__(self) -> None:
        self.app: Flask = None
        self.shortener = init_shortener()

    def setup_me(self, app: Flask) -> None:
        self.app = app
        self.main_route_register()
        self.api_route_register()
        self.preprocessor_context()

    def preprocessor_context(self):
        @self.app.context_processor
        def preprocessor_route():
            def register_url():
                return "/register"

            def login_url():
                return "/login"

            def dashboard_url():
                return "/dashboard"

            def toc_url():
                return "/toc"

            def pp_url():
                return "/privacy-policy"

            return dict(
                register_url=register_url(),
                login_url=login_url(),
                dashboard_url=dashboard_url,
                toc_url=toc_url(),
                pp_url=pp_url(),
            )

    def main_route_register(self):
        @self.app.route("/login")
        def login_page():
            return render_template("base/login.html")

        @self.app.route("/register")
        def register_page():
            return render_template("base/register.html")

        @self.app.route("/dashboard")
        def dashboard_page():
            return render_template("base/dashboard.html")

        @self.app.route("/admin")
        def admin_page():
            return render_template("base/admin.html")

        @self.app.route("/toc")
        def toc():
            return render_template("pages/rules/toc.html")

        @self.app.route("/privacy-policy")
        def pp():
            return render_template("/privacy-policy")

    def api_route_register(self) -> None:
        @self.app.route("/api/analytics/platform", methods=["GET"])
        def analytics_platform():
            return jsonify(
                {
                    "status": True,
                    "stats": {
                        "totalLinks": self.shortener.len_all_what(),
                        "totalUsers": self.shortener.len_all_what("user"),
                        "totalClicks": self.shortener.len_all_what("click"),
                        "totalCountries": self.shortener.len_all_what("visitor"),
                    },
                }
            )

        @self.app.route("/api/links/public", methods=["POST"])
        def pub_shorturl():
            a = request.get_json()
            data = self.shortener.create(123, a["longuri"])
            return jsonify(data), 200

        @self.app.route("/<code>", methods=["GET"])
        def redirect_link(code) -> None:
            # sanitize code must be str and other sanitize handled by custom protection library
            slug = str(code)
            
            pack_id = self.shortener.find_Packid_With_Shorten_ID(shorten_id=slug)
            data = self.shortener.get_redirect(pack_id=pack_id)
            return redirect(data)

        @self.app.route("/docs")
        def docs() -> None:
            return """
HOST: hosted IP or website, example : http://localhost:8001
BASE: [HOST]/api

SECURITY: NO RATELIMIT CURRENTLY

## Analytic
1. Stats
 method: ONLY GET
 endpoint : [BASE]/analytic/platform
 message : "stats server and counting how many links shortenedd, user registered, links clicked and visitor countries",
 response: json   

## Shortener service
1. Pub shortener
 method: ONLY POST
 endpoint: [BASE]/links/public
 message: "public shortener for guest user or just visitor"
 response: json
 
2. slug redirect
 method: ONLY GET
 endpoint: [HOST]/<slug>
 message: "redirect user into longURL or REAL URL"
 response: auto redirect
        
        """