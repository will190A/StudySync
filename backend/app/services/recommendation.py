from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
from app.db.session import SessionLocal
from app.models.question import Question
from app.models.user_answer import UserAnswer

class RecommendationService:
    def __init__(self):
        self.db = SessionLocal()
        
    def get_user_knowledge_profile(self, user_id: int) -> Dict[str, float]:
        """获取用户知识点掌握情况"""
        answers = self.db.query(UserAnswer).filter(UserAnswer.user_id == user_id).all()
        
        # 计算每个知识点的正确率
        knowledge_scores = {}
        for answer in answers:
            question = self.db.query(Question).get(answer.question_id)
            if question and question.knowledge_points:
                for point in question.knowledge_points:
                    if point not in knowledge_scores:
                        knowledge_scores[point] = {"correct": 0, "total": 0}
                    knowledge_scores[point]["total"] += 1
                    if answer.is_correct:
                        knowledge_scores[point]["correct"] += 1
        
        # 计算掌握度
        mastery = {}
        for point, scores in knowledge_scores.items():
            mastery[point] = scores["correct"] / scores["total"]
            
        return mastery
    
    def recommend_daily_practice(self, user_id: int, num_questions: int = 5) -> List[int]:
        """推荐每日练习题目"""
        # 获取用户知识点掌握情况
        mastery = self.get_user_knowledge_profile(user_id)
        
        # 获取所有题目
        questions = self.db.query(Question).all()
        
        # 计算每个题目的推荐分数
        question_scores = []
        for question in questions:
            score = 0
            if question.knowledge_points:
                # 计算题目相关知识点的最低掌握度
                min_mastery = min([mastery.get(point, 0.5) for point in question.knowledge_points])
                # 掌握度越低，推荐分数越高
                score = 1 - min_mastery
                # 考虑题目难度
                score *= (6 - question.difficulty) / 5
            question_scores.append((question.id, score))
        
        # 按推荐分数排序
        question_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 返回推荐题目ID
        return [q[0] for q in question_scores[:num_questions]]
    
    def generate_study_plan(self, user_id: int, target_date: str, daily_study_time: int) -> Dict[str, Any]:
        """生成学习计划"""
        # 获取用户知识点掌握情况
        mastery = self.get_user_knowledge_profile(user_id)
        
        # 找出需要加强的知识点
        weak_points = [point for point, score in mastery.items() if score < 0.7]
        
        # 获取相关题目
        questions = self.db.query(Question).filter(
            Question.knowledge_points.overlap(weak_points)
        ).all()
        
        # 按知识点和难度分组
        question_groups = {}
        for question in questions:
            for point in question.knowledge_points:
                if point in weak_points:
                    if point not in question_groups:
                        question_groups[point] = []
                    question_groups[point].append(question)
        
        # 生成学习任务
        tasks = []
        for point, point_questions in question_groups.items():
            # 每个知识点分配2-3个题目
            num_questions = min(3, len(point_questions))
            task_questions = np.random.choice(point_questions, num_questions, replace=False)
            tasks.append({
                "title": f"练习知识点：{point}",
                "question_ids": [q.id for q in task_questions]
            })
        
        return {
            "title": "智能学习计划",
            "description": f"针对薄弱知识点的强化练习计划",
            "tasks": tasks
        } 