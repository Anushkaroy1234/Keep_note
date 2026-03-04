import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings  # your pydantic settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


security = HTTPBearer()
# Create bcrypt context (for reference, but we'll use bcrypt directly)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#  Hash password
def hash_password(password: str) -> str:
    # Truncate password to 72 bytes max (bcrypt limitation)
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

#  Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to 72 bytes max (bcrypt limitation)
    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))



# JWT Functions

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY

# Create Access Token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Create Refresh Token
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verify any JWT token
def verify_token(token: str, token_type: str = "access") -> dict | None:
    """
    Verify JWT token and ensure type matches
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None
    




def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token, token_type="access")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload