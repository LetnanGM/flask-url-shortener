default_config = {
    "enable_fake_headers": True,  # fake headers for confusing tools automation from attacker's
    "enable_honeypot": True,  # honeypot for trapping hacker's
    "enable_ua_blocking": True,  # user-agent blocking for tools automation from attacker's
    "honeypot_delay": 3,  # seconds delay for waste attacker's time
    "auto_block_threshold": 3,  # honeypot hits before auto-block
}


# fake server name for confusing tools automation, add new name server for make complex
# it's work with headers scanning and key headers is 'server' or 'powered-by'
server_fake = [
    "nginx/1.18.0",
    "nginx/1.20.2",
    "nginx/1.21.6",
    "Apache/2.4.41",
    "Apache/2.4.54 (Ubuntu)",
    "Apache/2.4.52",
    "Microsoft-IIS/10.0",
    "LiteSpeed/5.4.12",
    "Caddy/2.6.2",
    "cloudflare",
    "openresty/1.19.9.1",
    "WowokRoyal/1.12.11",
]

# making server 'protected' but it's just confusing hacker's wkwkk :D
# i hope, nobody use this in production bruh :S
fake_headers_config = {
    "X-Powered-By": ["PHP/7.4.3", "PHP/8.1.2", "PHP/8.0.12", "ASP.NET"],
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "X-XSS-Protection": "1; mode=block",
}

# how to trap hacker's? use this :D
# honeypot routes, make hackers trapped and general information logged into your server
# you can block hacker's IP if hacker's attacking or exploiting your website :S
honeypot_routes = [
    # Admin panels
    "/admin",
    "/administrator",
    "/admin.php",
    "/admin/login",
    "/wp-admin",
    "/wp-login.php",
    "/wp-admin/admin-ajax.php",
    # Database managers
    "/phpmyadmin",
    "/pma",
    "/phpMyAdmin",
    "/mysql",
    "/adminer",
    "/adminer.php",
    "/db",
    "/database",
    # Config files
    "/.env",
    "/.env.local",
    "/.env.production",
    "/config.php",
    "/configuration.php",
    "/wp-config.php",
    "/.git/config",
    "/.git/HEAD",
    "/.aws/credentials",
    # Common exploits
    "/xmlrpc.php",
    "/phpinfo.php",
    "/info.php",
    "/shell.php",
    "/c99.php",
    "/r57.php",
    # Backup files
    "/backup.sql",
    "/backup.zip",
    "/database.sql",
    "/dump.sql",
    "/old",
    "/old.zip",
]

# it's BAD UA (User-Agent) patterns
# how it works? just add useragent toolkit automation, and it will blocked automatically
# can't handling if attacker's using random user-agent valid, just believe with honeypot :S
bad_ua_patterns = [
    # SQL Injection tools
    "sqlmap",
    "havij",
    "bsqlbf",
    # Vulnerability scanners
    "nikto",
    "nessus",
    "openvas",
    "acunetix",
    "netsparker",
    "qualys",
    "burp",
    "zap",
    "w3af",
    "nuclei",
    # Network scanners
    "nmap",
    "masscan",
    "zmap",
    "shodan",
    # CMS scanners
    "wpscan",
    "joomscan",
    "droopescan",
    # Directory brute force
    "dirbuster",
    "dirb",
    "gobuster",
    "ffuf",
    "wfuzz",
    # Web scanners
    "whatweb",
    "webinspect",
    "appscan",
    # Exploit frameworks
    "metasploit",
    "sqlninja",
    "pangolin",
    # Crawlers (aggressive)
    "scrapy",
    "curl",
    "wget",
    "python-requests",
    "go-http-client",
    "java/",
    "pycurl",
]
