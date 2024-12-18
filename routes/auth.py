from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.security import verify_password, create_access_token, AuthSettings, get_password_hash
from database.dependencies import get_db, get_current_active_admin
from database.session import org_id_ctx
from models.user import User
from schemas.request.AuthRequest import LoginRequest
from schemas.user import Token, UserResponse, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
    responses={404: {"description": "Not found"}}
)

@router.post("/token", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    # Get org_id from context (set by tenant middleware)
    org_id = org_id_ctx.get()
    if not org_id:
        raise HTTPException(
            status_code=400,
            detail="Organization context not found"
        )

    # Find user in specific organization
    user = db.query(User).filter(
        User.email == login_data.email,
        User.org_id == org_id
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "org_id": user.org_id,
            "email": user.email,
            "role": user.role
        },
        expires_delta=timedelta(minutes=AuthSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=access_token)

@router.post("/users", response_model=UserResponse)
async def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_active_admin)  # Only admins can create users
):
    # Get org_id from context
    org_id = org_id_ctx.get()
    if not org_id:
        raise HTTPException(
            status_code=400,
            detail="Organization context not found"
        )

    # Check if user already exists in this organization
    existing_user = db.query(User).filter(
        User.email == user_data.email,
        User.org_id == org_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered in this organization"
        )

    # Create new user - org_id is automatically handled by TenantAwareModel
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
        org_id=org_id  # Explicitly set the org_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user