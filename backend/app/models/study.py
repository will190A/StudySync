from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class UserAnswer(BaseModel):
    __tablename__ = "user_answers"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(JSON, nullable=False)  # 用户答案
    is_correct = Column(Boolean, nullable=False)
    time_spent = Column(Integer)  # 答题用时（秒）
    notes = Column(Text)  # 用户笔记
    
    # 关系
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="user_answers")

class StudyPlan(BaseModel):
    __tablename__ = "study_plans"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    daily_study_time = Column(Integer)  # 每日学习时间（分钟）
    status = Column(String(20), default="active")  # active, completed, paused
    is_ai_generated = Column(Boolean, default=False)
    
    # 关系
    user = relationship("User", back_populates="study_plans")
    tasks = relationship("StudyTask", back_populates="plan")

class StudyTask(BaseModel):
    __tablename__ = "study_tasks"
    
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
    status = Column(String(20), default="pending")  # pending, completed, skipped
    question_ids = Column(JSON)  # 关联的题目ID列表
    
    # 关系
    plan = relationship("StudyPlan", back_populates="tasks") 