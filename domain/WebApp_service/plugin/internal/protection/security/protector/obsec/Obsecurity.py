from flask import Flask, abort, request, jsonify
from functools import lru_cache
from collections import defaultdict

from ....data.configuration.security.config_obsecurity import (
    default_config,
    server_fake,
    fake_headers_config,
    honeypot_routes,
    bad_ua_patterns,
)
from ....utils.logging.childLogger import obs_logger

import random
import hashlib
import time
import werkzeug.serving


class OBSecurity:
    def __init__(self, app: Flask, config: dict = None) -> None:
        self.app = app

        self.config = {**default_config, **(config or {})}
        self.server_fake = server_fake
        self.fake_headers_config = fake_headers_config
        self.honeypot_routes = honeypot_routes
        self.bad_ua_patterns = bad_ua_patterns

        # IP blocking storage
        self.blocked_ips = set()
        self._honeypot_hits = defaultdict(int)

        self.obsec_routes()

    @lru_cache(maxsize=2048)
    def _is_bad_ua(self, ua: str) -> bool:
        """Cached user agent checking untuk performa"""
        ua_lower = ua.lower()
        return any(pattern in ua_lower for pattern in self.bad_ua_patterns)

    def _get_client_ip(self) -> str:
        """Get real client IP (consider proxy headers)"""
        # Check common proxy headers
        if request.headers.get("X-Forwarded-For"):
            return request.headers.get("X-Forwarded-For").split(",")[0].strip()
        elif request.headers.get("X-Real-IP"):
            return request.headers.get("X-Real-IP")
        elif request.headers.get("CF-Connecting-IP"):  # Cloudflare
            return request.headers.get("CF-Connecting-IP")
        return request.remote_addr or "unknown"

    def _generate_fingerprint(self) -> str:
        """Generate fingerprint dari request untuk tracking"""
        fp_data = f"{self._get_client_ip()}-{request.user_agent.string}"
        return hashlib.md5(fp_data.encode()).hexdigest()

    def obsec_routes(self):
        @self.app.before_request
        def security_checks():
            """Konsolidasi semua security checks"""
            client_ip = self._get_client_ip()

            # 1. IP Blocking check
            if client_ip in self.blocked_ips:
                obs_logger.vsilent(
                    f"⛔ BLOCKED IP attempted access: {client_ip} -> {request.path}"
                )
                abort(403)

            # 2. Bad User Agent Detection
            if self.config["enable_ua_blocking"]:
                ua = request.user_agent.string
                if self._is_bad_ua(ua):
                    obs_logger.vsilent(
                        f"🚨 BAD UA detected: {ua[:80]}... from {client_ip}"
                    )

                    # Random response untuk confuse scanner
                    fake_responses = [
                        (abort(403), None),
                        (abort(404), None),
                        (abort(500), None),
                        (jsonify({"error": "Forbidden"}), 403),
                        (jsonify({"error": "Not Found"}), 404),
                        ("Unauthorized", 401),
                        ("Bad Gateway", 502),
                    ]

                    response, code = random.choice(fake_responses)
                    if code:
                        return response, code
                    return response

        @self.app.after_request
        def fake_headers(response):
            """Inject fake headers untuk security through obscurity"""
            if not self.config["enable_fake_headers"]:
                return response

            # Random server signature setiap request
            server_sig = random.choice(self.server_fake)
            werkzeug.serving.WSGIRequestHandler.server_version = server_sig
            werkzeug.serving.WSGIRequestHandler.sys_version = ""

            # Add fake headers
            for name, value in self.fake_headers_config.items():
                if isinstance(value, list):
                    response.headers[name] = random.choice(value)
                else:
                    response.headers[name] = value

            # Remove revealing Flask headers
            response.headers.pop("Server", None)

            return response

        # Dynamic honeypot routes
        if self.config["enable_honeypot"]:

            def honeypot_handler():
                client_ip = self._get_client_ip()
                fingerprint = self._generate_fingerprint()

                obs_logger.vsilent(
                    f"🍯 HONEYPOT triggered: {request.path} | Method: {request.method} | IP: {client_ip}"
                )

                # Track honeypot hits
                self._honeypot_hits[fingerprint] += 1
                hit_count = self._honeypot_hits[fingerprint]

                # Auto-block after threshold
                if hit_count >= self.config["auto_block_threshold"]:
                    self.blocked_ips.add(client_ip)
                    obs_logger.vsilent(
                        f"🔒 IP AUTO-BLOCKED: {client_ip} ({hit_count} honeypot hits)"
                    )
                else:
                    obs_logger.vsilent(
                        f"📊 Honeypot hit #{hit_count} for fingerprint: {fingerprint[:16]}..."
                    )

                # Waste attacker's time
                time.sleep(self.config["honeypot_delay"])

                # Random realistic responses
                fake_responses = [
                    (abort(404), None),
                    (abort(403), None),
                    (abort(401), None),
                    (abort(500), None),
                    (jsonify({"error": "Not Found"}), 404),
                    (jsonify({"error": "Forbidden", "message": "Access Denied"}), 403),
                    (jsonify({"status": "error", "code": 401}), 401),
                    ("Unauthorized", 401),
                    ("Internal Server Error", 500),
                    ("<html><body><h1>404 Not Found</h1></body></html>", 404),
                ]

                response, code = random.choice(fake_responses)
                if code:
                    return response, code
                return response

            # Register semua honeypot routes
            for route in self.honeypot_routes:
                endpoint_name = f'honeypot_{route.replace("/", "_").replace(".", "_")}'
                self.app.add_url_rule(
                    route,
                    endpoint_name,
                    honeypot_handler,
                    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
                )
                # obs_logger.vsilent(f"🕸️  Honeypot deployed: {route}")

    def block_ip(self, ip: str):
        """Manually block an IP address"""
        self.blocked_ips.add(ip)
        obs_logger.vsilent(f"🔒 IP manually blocked: {ip}")

    def unblock_ip(self, ip: str):
        """Manually unblock an IP address"""
        if ip in self.blocked_ips:
            self.blocked_ips.discard(ip)
            obs_logger.vsilent(f"🔓 IP unblocked: {ip}")
        else:
            obs_logger.vsilent(f"⚠️  IP not in blocklist: {ip}")

    def get_blocked_ips(self) -> list:
        """Get list of blocked IPs"""
        return list(self.blocked_ips)

    def get_honeypot_stats(self) -> dict:
        """Get honeypot statistics"""
        return {
            "total_fingerprints": len(self._honeypot_hits),
            "total_hits": sum(self._honeypot_hits.values()),
            "blocked_ips_count": len(self.blocked_ips),
            "top_attackers": sorted(
                self._honeypot_hits.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    def clear_honeypot_stats(self):
        """Clear honeypot statistics (keep blocked IPs)"""
        self._honeypot_hits.clear()
        obs_logger.vsilent("📊 Honeypot statistics cleared")

    def reset_all(self):
        """Reset all - clear blocks and stats"""
        self.blocked_ips.clear()
        self._honeypot_hits.clear()
        obs_logger.vsilent("🔄 All security data reset")
