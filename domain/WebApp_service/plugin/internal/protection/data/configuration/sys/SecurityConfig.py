import re
from typing import Dict, List
from enum import Enum


class ThreatLevel(Enum):
    """Threat severity levels"""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class SecurityConfig:
    """
    Fortress-level Security Configuration
    Enterprise-grade protection dengan detection patterns yang comprehensive
    """

    # ============================================================================
    # RATE LIMITING - Multi-tiered protection
    # ============================================================================
    MAX_REQUESTS_PER_SECOND = 10  # Burst protection
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    MAX_REQUESTS_PER_DAY = 10000

    # Login protection
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_LOCKOUT_DURATION = 900  # 15 minutes
    MAX_LOGIN_ATTEMPTS_PER_HOUR = 20  # Across all users from same IP

    # API specific limits
    MAX_API_CALLS_PER_MINUTE = 100
    MAX_API_CALLS_PER_HOUR = 5000

    # Upload limits
    MAX_UPLOAD_SIZE_MB = 10
    MAX_UPLOADS_PER_HOUR = 50

    # ============================================================================
    # SQL INJECTION PATTERNS - Comprehensive detection
    # ============================================================================
    SQL_INJECTION_PATTERNS = [
        # Basic SQL keywords
        r"(\bunion\b.*\bselect\b)",
        r"(\bselect\b.*\bfrom\b)",
        r"(\binsert\b.*\binto\b)",
        r"(\bupdate\b.*\bset\b)",
        r"(\bdelete\b.*\bfrom\b)",
        r"(\bdrop\b.*\b(table|database|schema|index)\b)",
        r"(\btruncate\b.*\btable\b)",
        r"(\balter\b.*\btable\b)",
        r"(\bcreate\b.*\b(table|database|user)\b)",
        # Execution commands
        r"(\bexec\b|\bexecute\b)",
        r"(\bsp_executesql\b)",
        r"(\bxp_cmdshell\b)",
        r"(\bdbms_\w+\b)",
        # Comments and string manipulation
        r"(;.*--|\/\*.*\*\/)",
        r"(--[^\n]*)",
        r"(#[^\n]*)",
        r"(\/\*!.*\*\/)",  # MySQL conditional comments
        # Boolean-based blind SQL injection
        r"('|\")(\s)*(or|and)(\s)*('|\")",
        r"(\bor\b.*=.*)",
        r"(\band\b.*=.*)",
        r"(1=1|1='1'|'1'='1')",
        r"(1=0|1='0'|'1'='0')",
        r"(\bor\b\s+\d+\s*=\s*\d+)",
        r"(\band\b\s+\d+\s*=\s*\d+)",
        # Time-based blind SQL injection
        r"(\bwaitfor\b.*\bdelay\b)",
        r"(\bsleep\b\s*\()",
        r"(\bbenchmark\b\s*\()",
        r"(\bpg_sleep\b\s*\()",
        # Union-based injection
        r"(\bunion\b.*\ball\b.*\bselect\b)",
        r"(\bunion\b\s+select\b)",
        # Stacked queries
        r"(;\s*\w+\s+)",
        r"(;\s*drop\b)",
        r"(;\s*delete\b)",
        # Information schema queries
        r"(\binformation_schema\b)",
        r"(\bsys\b\.\w+)",
        r"(\bmysql\b\.\w+)",
        r"(\bpg_catalog\b)",
        # Hex encoding attempts
        r"(0x[0-9a-fA-F]+)",
        # SQL functions often used in injection
        r"(\bconcat\b\s*\()",
        r"(\bsubstring\b\s*\()",
        r"(\bchar\b\s*\()",
        r"(\bascii\b\s*\()",
        r"(\bload_file\b\s*\()",
        r"(\binto\b\s+\boutfile\b)",
        # Database fingerprinting
        r"(@@version)",
        r"(version\(\))",
        r"(\buser\b\s*\(\))",
        r"(\bdatabase\b\s*\(\))",
    ]

    # ============================================================================
    # XSS PATTERNS - Advanced detection including obfuscation
    # ============================================================================
    XSS_PATTERNS = [
        # Script tags (various encodings)
        r"<script[^>]*>.*?</script>",
        r"<script[^>]*>",
        r"</script>",
        r"%3Cscript",
        r"&lt;script",
        r"\\x3cscript",
        # JavaScript protocols
        r"javascript\s*:",
        r"jscript\s*:",
        r"vbscript\s*:",
        r"data\s*:\s*text/html",
        # Event handlers (comprehensive list)
        r"on\w+\s*=",  # Generic event handler
        r"onerror\s*=",
        r"onload\s*=",
        r"onclick\s*=",
        r"onmouseover\s*=",
        r"onmouseout\s*=",
        r"onfocus\s*=",
        r"onblur\s*=",
        r"onchange\s*=",
        r"onsubmit\s*=",
        r"onkeypress\s*=",
        r"onkeydown\s*=",
        r"onkeyup\s*=",
        r"onabort\s*=",
        r"ondrag\s*=",
        r"ondrop\s*=",
        r"onanimationend\s*=",
        # Dangerous tags
        r"<iframe",
        r"<frame",
        r"<frameset",
        r"<object",
        r"<embed",
        r"<applet",
        r"<meta",
        r"<link",
        r"<style",
        r"<base",
        r"<svg[^>]*>",
        r"<math[^>]*>",
        # HTML5 specific
        r"<video[^>]*>",
        r"<audio[^>]*>",
        r"<source[^>]*>",
        # Expression and CSS injection
        r"expression\s*\(",
        r"import\s*\(",
        r"@import",
        r"url\s*\(",
        r"behavior\s*:",
        # DOM-based XSS patterns
        r"(document\.)?(write|writeln|innerHTML|outerHTML)",
        r"eval\s*\(",
        r"setTimeout\s*\(",
        r"setInterval\s*\(",
        r"Function\s*\(",
        # Encoded variations
        r"&#\d+;",  # Decimal entities
        r"&#x[0-9a-fA-F]+;",  # Hex entities
        r"%[0-9a-fA-F]{2}",  # URL encoding
        r"\\u[0-9a-fA-F]{4}",  # Unicode escape
        r"\\x[0-9a-fA-F]{2}",  # Hex escape
    ]

    # ============================================================================
    # PATH TRAVERSAL PATTERNS - Comprehensive including encodings
    # ============================================================================
    PATH_TRAVERSAL_PATTERNS = [
        # Basic patterns
        r"\.\./",
        r"\.\.",
        r"\.\.\\",
        # URL encoded
        r"%2e%2e",
        r"%2e%2e/",
        r"%2e%2e\\",
        r"\.\.%2f",
        r"\.\.%5c",
        # Double URL encoded
        r"%252e%252e",
        r"%252e%252e%252f",
        r"%252e%252e%255c",
        # Unicode/UTF-8 encoded
        r"%c0%ae",
        r"%e0%80%ae",
        # Mixed encodings
        r"\.%2e/",
        r"%2e\./",
        r"\.%2e%2f",
        # Absolute paths (Unix)
        r"^/etc/",
        r"^/var/",
        r"^/usr/",
        r"^/home/",
        r"^/root/",
        r"^/proc/",
        r"^/sys/",
        # Absolute paths (Windows)
        r"^[a-zA-Z]:\\",
        r"^\\\\",
        # Special files
        r"/etc/passwd",
        r"/etc/shadow",
        r"/etc/hosts",
        r"\.\.\/\.\.\/",  # Multiple traversals
        r"\.\.\\\.\.\\",
        # Null byte injection
        r"%00",
        r"\\0",
    ]

    # ============================================================================
    # COMMAND INJECTION PATTERNS - OS command execution
    # ============================================================================
    COMMAND_INJECTION_PATTERNS = [
        # Shell operators
        r"[;&|`]",
        r"&&",
        r"\|\|",
        r"\|",
        r">\s*/dev/null",
        r"2>&1",
        # Command substitution
        r"\$\(.*\)",
        r"`.*`",
        r"\${.*}",
        # Shell variables
        r"\$\w+",
        r"\$\{.*\}",
        # File redirection
        r">\s*[/\w]+",
        r">>\s*[/\w]+",
        r"<\s*[/\w]+",
        # Common dangerous commands
        r"\b(cat|ls|dir|type|more|less|head|tail)\b",
        r"\b(rm|del|erase|rmdir)\b",
        r"\b(wget|curl|fetch)\b",
        r"\b(nc|netcat|ncat)\b",
        r"\b(chmod|chown|chgrp)\b",
        r"\b(ps|top|kill|pkill)\b",
        r"\b(su|sudo|runas)\b",
        r"\b(bash|sh|cmd|powershell|pwsh)\b",
        r"\b^(sudo )?(python|perl|ruby|php|node)( .*)?$\b",
        r"\b(eval|exec|system)\b",
        # Environment variables
        r"\$PATH",
        r"\$HOME",
        r"\$USER",
        r"%PATH%",
        r"%USERPROFILE%",
        # Piping and chaining
        r"\s*\|\s*",
        r"\s*;\s*",
        r"\s*&&\s*",
    ]

    # ============================================================================
    # LDAP INJECTION PATTERNS
    # ============================================================================
    LDAP_INJECTION_PATTERNS = [
        r"\*",
        r"\(",
        r"\)",
        r"\\",
        r"\|",
        r"&",
        r"(\(|\)|\*|\||&)",
        r"(\buid\b|\bcn\b|\bou\b|\bdc\b)=",
    ]

    # ============================================================================
    # XML/XXE PATTERNS
    # ============================================================================
    XXE_PATTERNS = [
        r"<!ENTITY",
        r"<!DOCTYPE",
        r"SYSTEM\s+[\"']file://",
        r"SYSTEM\s+[\"']http://",
        r"SYSTEM\s+[\"']https://",
        r"<!ELEMENT",
        r"<!ATTLIST",
        r"&\w+;",
    ]

    # ============================================================================
    # REMOTE CODE EXECUTION PATTERNS
    # ============================================================================
    RCE_PATTERNS = [
        # Deserialization
        r"(__import__|__builtins__|__globals__)",
        r"(pickle|cPickle|marshal|shelve)",
        r"(unserialize|deserialize)",
        # Code execution functions
        r"\beval\s*\(",
        r"\bexec\s*\(",
        r"\bcompile\s*\(",
        r"\b__import__\s*\(",
        # Template injection
        r"\{\{.*\}\}",
        r"\{%.*%\}",
        r"\${.*}",
        # Python specific
        r"os\.system",
        r"subprocess\.",
        r"commands\.",
        # PHP specific
        r"system\s*\(",
        r"shell_exec\s*\(",
        r"passthru\s*\(",
        r"proc_open\s*\(",
        r"popen\s*\(",
    ]

    # ============================================================================
    # SSRF (Server-Side Request Forgery) PATTERNS
    # ============================================================================
    SSRF_PATTERNS = [
        # Localhost variations
        r"localhost",
        r"127\.0\.0\.1",
        r"0\.0\.0\.0",
        r"::1",
        r"0:0:0:0:0:0:0:1",
        # Private IP ranges
        r"10\.\d+\.\d+\.\d+",
        r"172\.(1[6-9]|2\d|3[01])\.\d+\.\d+",
        r"192\.168\.\d+\.\d+",
        # Cloud metadata endpoints
        r"169\.254\.169\.254",  # AWS, Azure, GCP
        r"metadata\.google\.internal",
        # File protocols
        r"file://",
        r"gopher://",
        r"dict://",
        r"ftp://",
    ]

    # ============================================================================
    # OPEN REDIRECT PATTERNS
    # ============================================================================
    OPEN_REDIRECT_PATTERNS = [
        r"(https?:)?//",
        r"javascript:",
        r"data:",
        r"%0d%0a",  # CRLF injection
        r"\\r\\n",
    ]

    # ============================================================================
    # SESSION FIXATION PATTERNS
    # ============================================================================
    SESSION_FIXATION_PATTERNS = [
        r"PHPSESSID=",
        r"JSESSIONID=",
        r"ASP\.NET_SessionId=",
        r"session_id=",
    ]

    # ============================================================================
    # MALICIOUS FILE UPLOAD PATTERNS
    # ============================================================================
    DANGEROUS_EXTENSIONS = {
        # Executables
        "exe",
        "dll",
        "bat",
        "cmd",
        "com",
        "msi",
        "scr",
        "vbs",
        "js",
        # Scripts
        "php",
        "phtml",
        "php3",
        "php4",
        "php5",
        "phps",
        "pht",
        "asp",
        "aspx",
        "cer",
        "asa",
        "asax",
        "ashx",
        "asmx",
        "jsp",
        "jspx",
        "jsw",
        "jsv",
        "jspf",
        "py",
        "pyc",
        "pyo",
        "rb",
        "pl",
        "cgi",
        # Shell scripts
        "sh",
        "bash",
        "ksh",
        "csh",
        "ps1",
        # Archives that could contain malware
        "jar",
        "war",
        "ear",
        # Other dangerous
        "swf",
        "htaccess",
        "htpasswd",
        "ini",
        "config",
    }

    SAFE_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "svg",
        "webp",
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "txt",
        "csv",
        "json",
        "xml",
        "mp3",
        "mp4",
        "avi",
        "mov",
        "wmv",
        "zip",
        "rar",
        "7z",
        "tar",
        "gz",
    }

    # Magic bytes untuk file validation
    MAGIC_BYTES = {
        "jpg": [b"\xff\xd8\xff"],
        "png": [b"\x89\x50\x4e\x47"],
        "gif": [b"GIF87a", b"GIF89a"],
        "pdf": [b"%PDF-"],
        "zip": [b"PK\x03\x04", b"PK\x05\x06"],
    }

    # ============================================================================
    # USER AGENT PATTERNS - Bot detection
    # ============================================================================
    SUSPICIOUS_USER_AGENTS = [
        r"bot",
        r"crawler",
        r"spider",
        r"scraper",
        r"curl",
        r"wget",
        r"python",
        r"java",
        r"perl",
        r"ruby",
        r"go-http-client",
        r"postman",
        r"insomnia",
        r"nikto",
        r"sqlmap",
        r"nmap",
        r"masscan",
        r"metasploit",
        r"burp",
        r"owasp",
    ]

    # ============================================================================
    # SECURITY HEADERS - Fortress-grade
    # ============================================================================
    SECURITY_HEADERS = {
        # XSS Protection
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        # HTTPS Enforcement
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        # Content Security Policy (strict)
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "upgrade-insecure-requests;"
        ),
        # Referrer Policy
        "Referrer-Policy": "strict-origin-when-cross-origin",
        # Permissions Policy (formerly Feature-Policy)
        "Permissions-Policy": (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        ),
        # Additional security headers
        "X-Permitted-Cross-Domain-Policies": "none",
        "X-Download-Options": "noopen",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Resource-Policy": "same-origin",
    }

    # ============================================================================
    # THREAT SCORING - Berdasarkan severity
    # ============================================================================
    THREAT_SCORES = {
        "sql_injection": ThreatLevel.CRITICAL,
        "xss": ThreatLevel.HIGH,
        "path_traversal": ThreatLevel.HIGH,
        "command_injection": ThreatLevel.CRITICAL,
        "rce": ThreatLevel.CRITICAL,
        "xxe": ThreatLevel.HIGH,
        "ssrf": ThreatLevel.HIGH,
        "ldap_injection": ThreatLevel.MEDIUM,
        "open_redirect": ThreatLevel.MEDIUM,
        "session_fixation": ThreatLevel.MEDIUM,
        "malicious_upload": ThreatLevel.HIGH,
        "rate_limit_exceeded": ThreatLevel.LOW,
    }

    # ============================================================================
    # WHITELISTS & BLACKLISTS
    # ============================================================================

    # IP Whitelist (trusted IPs yang tidak akan di-rate limit)
    WHITELISTED_IPS = [
        "127.0.0.1",
        "::1",
    ]

    # state methods
    STATE_METHODS_REQ = ["PUT", "DELETE", "PATH", "POST"]

    # IP Blacklist (permanent block)
    BLACKLISTED_IPS = set()

    # Trusted origin (origin yang dipercaya)
    TRUSTED_ORIGIN = ["http://google.com", "http://localhost:5000"]

    # Endpoint yang tidak butuh CSRF protection
    CSRF_EXEMPT_ENDPOINTS = [
        "/health_check/",
        "/api.public/",
        "/webhook/",
        "/api/",
        "/apiv2/",
    ]

    # ============================================================================
    # MONITORING & ALERTING THRESHOLDS
    # ============================================================================

    # Alert ketika threshold ini tercapai
    ALERT_THRESHOLD_ATTACKS_PER_HOUR = 50
    ALERT_THRESHOLD_UNIQUE_IPS = 20
    ALERT_THRESHOLD_FAILED_LOGINS = 10

    # Auto-ban threshold
    AUTO_BAN_THRESHOLD = 10  # Violations sebelum auto-ban
    AUTO_BAN_DURATION_HOURS = 24

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    @classmethod
    def compile_patterns(cls) -> Dict[str, List[re.Pattern]]:
        """Compile semua regex patterns untuk performa lebih baik"""
        compiled = {}

        pattern_groups = {
            "sql_injection": cls.SQL_INJECTION_PATTERNS,
            "xss": cls.XSS_PATTERNS,
            "path_traversal": cls.PATH_TRAVERSAL_PATTERNS,
            "command_injection": cls.COMMAND_INJECTION_PATTERNS,
            "ldap_injection": cls.LDAP_INJECTION_PATTERNS,
            "xxe": cls.XXE_PATTERNS,
            "rce": cls.RCE_PATTERNS,
            "ssrf": cls.SSRF_PATTERNS,
            "open_redirect": cls.OPEN_REDIRECT_PATTERNS,
        }

        for name, patterns in pattern_groups.items():
            compiled[name] = [
                re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in patterns
            ]

        return compiled

    @classmethod
    def is_extension_safe(cls, filename: str) -> bool:
        """Check apakah extension file aman"""
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        # Prioritas: check dangerous first
        if ext in cls.DANGEROUS_EXTENSIONS:
            return False

        # Jika ada di safe list, allow
        if ext in cls.SAFE_EXTENSIONS:
            return True

        # Unknown extension = suspicious
        return False

    @classmethod
    def verify_file_magic_bytes(cls, file_content: bytes, declared_ext: str) -> bool:
        """Verify file magic bytes matches declared extension"""
        if declared_ext not in cls.MAGIC_BYTES:
            return True  # Can't verify, allow (akan di-check di layer lain)

        magic_patterns = cls.MAGIC_BYTES[declared_ext]
        return any(file_content.startswith(pattern) for pattern in magic_patterns)

    @classmethod
    def get_threat_score(cls, threat_type: str) -> int:
        """Get numeric threat score"""
        threat_level = cls.THREAT_SCORES.get(threat_type, ThreatLevel.LOW)
        return threat_level.value
