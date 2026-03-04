# ...existing code...
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.security import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        if request.url.path in ["/auth/login", "/auth/signup", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})
        
        scheme, token = get_authorization_scheme_param(auth_header)
        if not scheme or scheme.lower() != "bearer" or not token:
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing auth token"})
        
        payload = verify_token(token, token_type="access")
        if not payload:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
        
        # Attach user info to request
        request.state.user = payload
        return await call_next(request)
