from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Question(BaseModel):
    __tablename__ = "questions"
    
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)  # single_choice, multiple_choice, true_false, programming
    options = Column(JSON)  # 选项，JSON格式
    correct_answer = Column(JSON, nullable=False)  # 正确答案，JSON格式
    explanation = Column(Text)  # 解析
    difficulty = Column(Integer)  # 难度等级 1-5
    knowledge_points = Column(JSON)  # 知识点标签
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    
    # 关系
    chapter = relationship("Chapter", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question")

class Chapter(BaseModel):
    __tablename__ = "chapters"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    
    # 关系
    questions = relationship("Question", back_populates="chapter")
    parent = relationship("Chapter", remote_side=[id], backref="children") 