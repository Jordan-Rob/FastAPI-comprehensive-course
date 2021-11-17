from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "37896804f3aa2a1795cbe0650aac5cb7d6c083706c309aa72ec3888ea60b6d4e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("user_id")

        if id is None:
            raise cred_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise cred_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, cred_exception )

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user