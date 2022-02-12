from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from . import schemas
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer


OAuth2Scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "62bead1112b0b0b98f060292843696a4efa22ec29909bf04729a1841224d3e1b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('username')
        userID = payload.get('id')
        if username is None or userID is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username,id=userID)
    except JWTError:
        raise credentials_exception
    return token_data
    
def getCurrentUser(token:str = Depends(OAuth2Scheme)):
    credentialE = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED\
                                ,detail="Invalid Credentials"\
                                ,headers={"Authorization":"Bearer"})
    return verify_token(token,credentialE)