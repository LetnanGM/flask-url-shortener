from datetime import datetime
from typing import List, Dict, Set
from collections import defaultdict
from .csrf_conf import CSRFViolation, TokenMetadata


class CSRFPriv:
    # Tracking dictionaries
    violations: List[CSRFViolation] = []
    suspicious_ips: Dict[str, int] = defaultdict(int)
    blocked_ips: Dict[str, datetime] = {}
    token_metadata: Dict[str, TokenMetadata] = {}

    # Attack pattern detection
    csrf_attack_patterns: Dict[str, List[datetime]] = defaultdict(list)
    compromised_tokens: Set[str] = set()

    TOKEN_EXPIRY_HOURS = 2
    MAX_TOKEN_USAGE = 50  # max times a token can be reused
    SUSPICIOUS_THRESHOLD = 3  # Failed attempts before marking as suspicious
