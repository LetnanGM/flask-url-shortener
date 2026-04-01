from share.shared.logger.print import Logger

protector_logger = Logger(
    log_file="assets/logs/Protector/protect/Session-protector-[time].log"
)
iv_logger = Logger("assets/logs/Protector/inputvalidator/iv-[time].log")
rl_logger = Logger(log_file="assets/logs/Protector/RateLimiter/limiter-[time].log")
obs_logger = Logger(log_file="assets/logs/Protector/OBSecurity/obs-[time].log")
chainring_logger = Logger(log_file="assets/logs/Protector/chainring/Chain-[time].log")
SMiddleware_logger = Logger(
    log_file="assets/logs/Protector/SecurityMiddleware/SMiddleware-[time].log"
)
global_protection_logger = Logger(log_file="assets/logs/protections/global-[time].log")
CSRFLogger = Logger(log_file="assets/logs/Protector/CSRF/CSRF-[time].log")
