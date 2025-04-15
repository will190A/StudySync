from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    last_login = Column(DateTime)
    streak_days = Column(Integer, default=0)  # 连续打卡天数
    last_check_in = Column(DateTime)  # 上次打卡时间 