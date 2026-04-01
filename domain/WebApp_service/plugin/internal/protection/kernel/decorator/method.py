from functools import wraps
from flask import request

def skip_for_safe_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return
        
        return func(*args, **kwargs)
    
    return wrapper
        