from ....utils.core_module.csrf import GEN

DYNAMIC_CONTEXT = {"csrf_token": GEN.generate_csrf_token}
