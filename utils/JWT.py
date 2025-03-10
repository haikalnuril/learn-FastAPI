import jwt
from datetime import timedelta, datetime
from typing import Optional
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY_JWT")
ALGORITHM = getenv("ALGORITHM_JWT")
EXPIRES_TOKEN_IN = int(getenv("EXPIRES_TOKEN_IN"))

def JWT_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(days=EXPIRES_TOKEN_IN)
    
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt