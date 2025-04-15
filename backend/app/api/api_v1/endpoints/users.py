from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash, verify_password
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 检查邮箱是否已存在
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 更新用户信息
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/check-in")
def user_check_in(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    
    # 检查是否可以打卡
    if current_user.last_check_in:
        last_check_in = current_user.last_check_in
        now = datetime.utcnow()
        if (now - last_check_in).days < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already checked in today"
            )
        elif (now - last_check_in).days == 1:
            current_user.streak_days += 1
        else:
            current_user.streak_days = 1
    
    # 更新打卡信息
    current_user.last_check_in = datetime.utcnow()
    current_user.experience += 10  # 每次打卡获得10点经验
    
    # 检查是否升级
    level_up_experience = current_user.level * 100
    if current_user.experience >= level_up_experience:
        current_user.level += 1
    
    db.commit()
    return {"message": "Check-in successful", "streak_days": current_user.streak_days} 