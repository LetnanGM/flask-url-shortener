from functools import wraps
from typing import Dict, Tuple
from flask import request
from .privilege import privilege

class Session:
    def __init__(self) -> None:
        self._sessions: Dict[str, str] = {}
    
    @property
    def get_sessions(self):
        return self._sessions
    
    def is_session_defined(self, session_id: str):
        return True if session_id not in self._sessions else False
    
    def get_session_by_userId(self, user_id: str) -> str | bool:
        if user_id not in self._sessions:
            return False
        
        for session, address in self._sessions.items():
            if user_id == address:
                return session
            
        return False
    
    def add_session(self, user_id: str) -> Tuple[bool, str]:
        from share.support.generator.uuid import uid
        
        if user_id in self._sessions:
            return True, self._sessions[self.get_session_by_userId(user_id)]
    
        session_id = uid.token_uuid()
        self._sessions[session_id] = user_id
        
        return True, session_id
    
    def remove_session(self, session_id: str) -> bool:
        session =  str([self._sessions[session_id] if session_id in self._sessions else None])
        if not session:
            return False
        
        del self._sessions[session]
        return True
    
class MSession(Session):
    def __init__(self):
        super().__init__()
        self._ms = privilege()
        
    @property
    def _session():
        return request.cookies.get("session_id")
        
    @property
    def is_authenticated(self):
        return True if self.is_session_defined(self._session) else False
    
    @property
    def is_authenticated_as_what(self): 
        """ """
        
        user_id = self._sessions[self._session]
        privilege = self._ms.take_info_user(user_id).privilege
        return privilege
    
    @property
    def is_admin(self) -> bool:
        return False if self.is_authenticated_as_what != "admin" else True
    
    @property
    def is_guest(self) -> bool:
        return False if self.is_authenticated_as_what != "guest" else True
    

def require_auth(privilege: str = "guest"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Auth = MSession()
            
            if not Auth.is_authenticated:
                return "Unauthorzied", 401
            
            if Auth.is_authenticated_as_what == privilege.lower():
                return "Unauthorized", 401
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
            