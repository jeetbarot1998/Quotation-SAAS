from typing import Type

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.security import verify_token
from database.session import SessionLocal
from models.user import User
from schemas.user import TokenData


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        token_data: TokenData = Depends(verify_token),
        db: Session = Depends(get_db)
) -> Type[User]:
    user = db.query(User).filter(
        User.id == token_data.user_id,
        User.org_id == token_data.org_id
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_admin(
        current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return current_user