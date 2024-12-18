from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database.session import org_id_ctx
from schemas.user import TokenData

# Security configurations
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthSettings:
    SECRET_KEY = "xCpuoUwWT4j2KQMQNrXLYR0Tg+IxrLvGyVL8KqBHO+I="
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if isinstance(to_encode.get("user_id"), str):
        to_encode["user_id"] = int(to_encode["user_id"])
    if isinstance(to_encode.get("org_id"), str):
        to_encode["org_id"] = int(to_encode["org_id"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=AuthSettings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        AuthSettings.SECRET_KEY,
        algorithm=AuthSettings.ALGORITHM
    )
    return encoded_jwt


async def verify_token(
        credentials: HTTPAuthorizationCredentials = Security(security)
) -> TokenData:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            AuthSettings.SECRET_KEY,
            algorithms=[AuthSettings.ALGORITHM]
        )

        user_id = int(payload.get("user_id"))
        org_id = int(payload.get("org_id"))
        email = payload.get("email")
        role = payload.get("role")

        if user_id is None or org_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        token_data = TokenData(
            user_id=user_id,
            org_id=org_id,
            email=email,
            role=role
        )

        # Set organization context
        org_id_ctx.set(org_id)

        return token_data

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )