from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "37896804f3aa2a1795cbe0650aac5cb7d6c083706c309aa72ec3888ea60b6d4e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

    