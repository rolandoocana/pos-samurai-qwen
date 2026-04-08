from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from . import config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_token(data: dict): return jwt.encode({**data, "exp": datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)}, config.JWT_SECRET, algorithm=config.ALGORITHM)
def hash_password(plain: str) -> str: return pwd_context.hash(plain)
