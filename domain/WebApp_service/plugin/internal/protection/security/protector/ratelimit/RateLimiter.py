from ....data.configuration.sys.SecurityConfig import SecurityConfig
from ....utils.logging.childLogger import rl_logger
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import hashlib
from dataclasses import dataclass, field


@dataclass
class RequestPattern:
    """Track request patterns for anomaly detection"""

    timestamps: List[datetime] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    user_agents: Set[str] = field(default_factory=set)
    request_signatures: List[str] = field(default_factory=list)

    def get_entropy_score(self) -> float:
        """Calculate pattern entropy (lower = more suspicious)"""
        if not self.timestamps:
            return 1.0

        # Check for timing patterns (bots often have regular intervals)
        if len(self.timestamps) >= 3:
            intervals = [
                (self.timestamps[i + 1] - self.timestamps[i]).total_seconds()
                for i in range(len(self.timestamps) - 1)
            ]
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)

            # Low variance = suspicious regular pattern
            if variance < 0.1:
                return 0.3

        # Check endpoint diversity
        unique_endpoints = len(set(self.endpoints))
        endpoint_diversity = unique_endpoints / max(len(self.endpoints), 1)

        # Check user agent consistency
        ua_diversity = len(self.user_agents) / max(len(self.timestamps), 1)

        return (endpoint_diversity + ua_diversity) / 2


@dataclass
class AttackCluster:
    """Track distributed attack clusters"""

    ips: Set[str] = field(default_factory=set)
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    attack_signature: str = ""
    severity: int = 0


class RateLimiter:
    """
    Advanced rate limiter with distributed attack detection.

    Features:
    - Traditional rate limiting per IP
    - Distributed attack detection across multiple IPs
    - Request pattern analysis
    - Fingerprint-based blocking
    - Adaptive thresholds
    - Attack cluster identification
    """

    def __init__(self):
        # Traditional tracking
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self.login_attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.blocked_ips: Dict[str, datetime] = {}

        # Smart tracking
        self.request_patterns: Dict[str, RequestPattern] = defaultdict(RequestPattern)
        self.suspicious_ips: Set[str] = set()
        self.fingerprint_blocks: Dict[str, datetime] = {}

        # Distributed attack detection
        self.attack_clusters: List[AttackCluster] = []
        self.global_request_buffer: List[Tuple[datetime, str, str]] = (
            []
        )  # (time, ip, signature)
        self.coordinated_ips: Set[str] = set()

        # Adaptive thresholds
        self.baseline_request_rate = 0
        self.anomaly_threshold = 1.5  # 150% of baseline

    def _generate_request_fingerprint(
        self, ip: str, user_agent: str = "", endpoint: str = "", method: str = ""
    ) -> str:
        """Generate unique fingerprint for request pattern"""
        signature = f"{user_agent}|{endpoint}|{method}"
        return hashlib.md5(signature.encode()).hexdigest()[:16]

    def _detect_distributed_attack(self) -> bool:
        """Detect coordinated attacks from multiple IPs"""
        now = datetime.now()

        # Clean old buffer (last 5 minutes)
        self.global_request_buffer = [
            (ts, ip, sig)
            for ts, ip, sig in self.global_request_buffer
            if now - ts < timedelta(minutes=5)
        ]

        if len(self.global_request_buffer) < 10:
            return False

        # Group by signature
        signature_groups: Dict[str, List[str]] = defaultdict(list)
        for _, ip, sig in self.global_request_buffer:
            signature_groups[sig].append(ip)

        # Detect suspicious patterns
        for signature, ips in signature_groups.items():
            unique_ips = set(ips)

            # Multiple IPs with same signature = potential distributed attack
            if len(unique_ips) >= 5 and len(ips) >= 20:
                # Create or update attack cluster
                self._register_attack_cluster(unique_ips, signature)
                rl_logger.vsilent(
                    f"🚨 DISTRIBUTED ATTACK DETECTED: {len(unique_ips)} IPs, "
                    f"signature: {signature[:8]}...",
                    extra={"ips": list(unique_ips)[:10], "signature": signature},
                )
                return True

        return False

    def _register_attack_cluster(self, ips: Set[str], signature: str):
        """Register a detected attack cluster"""
        now = datetime.now()

        # Check if cluster already exists
        for cluster in self.attack_clusters:
            if cluster.attack_signature == signature:
                cluster.ips.update(ips)
                cluster.last_seen = now
                cluster.severity += 1
                self.coordinated_ips.update(ips)
                return

        # Create new cluster
        new_cluster = AttackCluster(
            ips=ips.copy(),
            first_seen=now,
            last_seen=now,
            attack_signature=signature,
            severity=1,
        )
        self.attack_clusters.append(new_cluster)
        self.coordinated_ips.update(ips)

        # Auto-block IPs in high-severity clusters
        if new_cluster.severity >= 3:
            for ip in ips:
                self.blocked_ips[ip] = now + timedelta(hours=1)

    def _analyze_request_pattern(self, ip: str) -> Tuple[bool, float]:
        """Analyze request pattern for suspicious behavior"""
        pattern = self.request_patterns[ip]

        if len(pattern.timestamps) < 5:
            return False, 1.0

        entropy = pattern.get_entropy_score()

        # Low entropy = suspicious bot-like behavior
        if entropy < 0.4:
            self.suspicious_ips.add(ip)
            rl_logger.vsilent(
                f"⚠️  Suspicious pattern detected for IP: {ip} (entropy: {entropy:.2f})",
                extra={"ip": ip, "entropy": entropy},
            )
            return True, entropy

        return False, entropy

    def is_blocked(self, ip: str) -> bool:
        """Check if IP is blocked (traditional or smart blocking)"""
        now = datetime.now()

        # Check traditional block
        if ip in self.blocked_ips:
            if now < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]

        # Check if part of coordinated attack
        if ip in self.coordinated_ips:
            # Check if still in active cluster
            for cluster in self.attack_clusters:
                if ip in cluster.ips and now - cluster.last_seen < timedelta(
                    minutes=30
                ):
                    rl_logger.vsilent(
                        f"🚫 Blocked coordinated attack IP: {ip}",
                        extra={"ip": ip, "cluster": cluster.attack_signature[:8]},
                    )
                    return True

            # Remove from coordinated if no active cluster
            self.coordinated_ips.discard(ip)

        return False

    def check_rate_limit(
        self, ip: str, user_agent: str = "", endpoint: str = "", method: str = "GET"
    ) -> bool:
        """Enhanced rate limit check with pattern analysis"""

        # di izinkan jika itu adalah IP admin
        if ip in SecurityConfig.WHITELISTED_IPS:
            # di izinkan
            return True

        now = datetime.now()

        # Generate request fingerprint
        fingerprint = self._generate_request_fingerprint(
            ip, user_agent, endpoint, method
        )

        # Check fingerprint blocks
        if fingerprint in self.fingerprint_blocks:
            if now < self.fingerprint_blocks[fingerprint]:
                rl_logger.vsilent(
                    f"🔒 Blocked by fingerprint: {fingerprint[:8]}... from IP: {ip}",
                    extra={"ip": ip, "fingerprint": fingerprint},
                )
                return False
            else:
                del self.fingerprint_blocks[fingerprint]

        # Add to global buffer for distributed detection
        self.global_request_buffer.append((now, ip, fingerprint))

        # Detect distributed attacks
        if self._detect_distributed_attack():
            # Block this IP if part of attack
            if ip in self.coordinated_ips:
                return False

        # Clean old requests
        self.requests[ip] = [
            req_time
            for req_time in self.requests[ip]
            if now - req_time < timedelta(hours=1)
        ]

        # Update pattern tracking
        pattern = self.request_patterns[ip]
        pattern.timestamps.append(now)
        pattern.endpoints.append(endpoint)
        pattern.user_agents.add(user_agent)
        pattern.request_signatures.append(fingerprint)

        # Keep only recent pattern data
        if len(pattern.timestamps) > 100:
            pattern.timestamps = pattern.timestamps[-100:]
            pattern.endpoints = pattern.endpoints[-100:]
            pattern.request_signatures = pattern.request_signatures[-100:]

        # Analyze pattern
        is_suspicious, entropy = self._analyze_request_pattern(ip)

        # Stricter limits for suspicious IPs
        max_per_minute = SecurityConfig.MAX_REQUESTS_PER_MINUTE
        max_per_hour = SecurityConfig.MAX_REQUESTS_PER_HOUR

        if is_suspicious:
            max_per_minute = max_per_minute // 2
            max_per_hour = max_per_hour // 2

        # Check limits
        recent_minute = [
            req_time
            for req_time in self.requests[ip]
            if now - req_time < timedelta(minutes=1)
        ]

        if len(recent_minute) >= max_per_minute:
            # Block fingerprint if repeated violations
            if len(recent_minute) >= max_per_minute * 2:
                self.fingerprint_blocks[fingerprint] = now + timedelta(minutes=30)

            rl_logger.vsilent(
                f"⛔ Rate limit exceeded (per minute) for IP: {ip} "
                f"[{len(recent_minute)}/{max_per_minute}] {'[SUSPICIOUS]' if is_suspicious else ''}",
                extra={
                    "ip": ip,
                    "count": len(recent_minute),
                    "suspicious": is_suspicious,
                },
            )
            return False

        if len(self.requests[ip]) >= max_per_hour:
            rl_logger.vsilent(
                f"⛔ Rate limit exceeded (per hour) for IP: {ip} "
                f"[{len(self.requests[ip])}/{max_per_hour}] {'[SUSPICIOUS]' if is_suspicious else ''}",
                extra={
                    "ip": ip,
                    "count": len(self.requests[ip]),
                    "suspicious": is_suspicious,
                },
            )
            return False

        self.requests[ip].append(now)
        return True

    def check_login_attempts(self, ip: str, username: str = "") -> bool:
        """Enhanced login attempt tracking with distributed detection"""
        now = datetime.now()

        # Clean old attempts
        self.login_attempts[ip] = [
            attempt_time
            for attempt_time in self.login_attempts[ip]
            if now - attempt_time
            < timedelta(seconds=SecurityConfig.LOGIN_LOCKOUT_DURATION)
        ]

        # Check for distributed brute force (many IPs, same username)
        if username:
            recent_username_attempts = sum(
                1
                for other_ip in self.login_attempts
                if other_ip != ip and self.login_attempts[other_ip]
            )

            if recent_username_attempts >= 10:
                rl_logger.vsilent(
                    f"🚨 DISTRIBUTED BRUTE FORCE detected on username: {username} "
                    f"from {recent_username_attempts} different IPs",
                    extra={"username": username, "ip_count": recent_username_attempts},
                )
                # Stricter limit during distributed attack
                if (
                    len(self.login_attempts[ip])
                    >= SecurityConfig.MAX_LOGIN_ATTEMPTS // 2
                ):
                    self.blocked_ips[ip] = now + timedelta(hours=2)
                    return False

        if len(self.login_attempts[ip]) >= SecurityConfig.MAX_LOGIN_ATTEMPTS:
            self.blocked_ips[ip] = now + timedelta(
                seconds=SecurityConfig.LOGIN_LOCKOUT_DURATION
            )
            rl_logger.vsilent(
                f"🔒 Too many login attempts. IP blocked: {ip}", extra={"ip": ip}
            )
            return False

        return True

    def record_login_attempt(self, ip: str):
        """Record a failed login attempt"""
        self.login_attempts[ip].append(datetime.now())

    def get_attack_statistics(self) -> Dict:
        """Get current attack statistics"""
        now = datetime.now()

        active_clusters = [
            cluster
            for cluster in self.attack_clusters
            if now - cluster.last_seen < timedelta(minutes=30)
        ]

        return {
            "blocked_ips": len(self.blocked_ips),
            "suspicious_ips": len(self.suspicious_ips),
            "coordinated_ips": len(self.coordinated_ips),
            "active_clusters": len(active_clusters),
            "fingerprint_blocks": len(self.fingerprint_blocks),
            "total_requests_tracked": sum(len(reqs) for reqs in self.requests.values()),
        }

    def cleanup_old_data(self):
        """Periodic cleanup of old tracking data"""
        now = datetime.now()

        # Clean old clusters
        self.attack_clusters = [
            cluster
            for cluster in self.attack_clusters
            if now - cluster.last_seen < timedelta(hours=24)
        ]

        # Clean old pattern data
        for ip in list(self.request_patterns.keys()):
            pattern = self.request_patterns[ip]
            if pattern.timestamps and now - pattern.timestamps[-1] > timedelta(hours=2):
                del self.request_patterns[ip]

        # Clean suspicious IPs that are no longer active
        self.suspicious_ips = {
            ip for ip in self.suspicious_ips if ip in self.request_patterns
        }

        rl_logger.vsilent("🧹 Cleaned up old rate limiter data")
