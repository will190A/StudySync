from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.study import StudyPlan, StudyTask
from app.schemas.study import (
    StudyPlanCreate,
    StudyPlanUpdate,
    StudyPlanResponse,
    StudyTaskCreate,
    StudyTaskUpdate,
    StudyTaskResponse
)
from app.core.auth import get_current_user
from app.services.recommendation import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.post("/generate", response_model=StudyPlanResponse)
def generate_study_plan(
    target_date: str,
    daily_study_time: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成智能学习计划"""
    plan_data = recommendation_service.generate_study_plan(
        current_user.id,
        target_date,
        daily_study_time
    )
    
    # 创建学习计划
    study_plan = StudyPlan(
        user_id=current_user.id,
        title=plan_data["title"],
        description=plan_data["description"],
        start_date=datetime.utcnow(),
        end_date=target_date,
        daily_study_time=daily_study_time,
        is_ai_generated=True
    )
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)
    
    # 创建学习任务
    for task_data in plan_data["tasks"]:
        task = StudyTask(
            plan_id=study_plan.id,
            title=task_data["title"],
            question_ids=task_data["question_ids"],
            scheduled_date=datetime.utcnow()  # 需要根据计划时间分配
        )
        db.add(task)
    
    db.commit()
    return study_plan

@router.get("/my-plans", response_model=List[StudyPlanResponse])
def get_my_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我的学习计划"""
    plans = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id
    ).all()
    return plans

@router.get("/plan/{plan_id}", response_model=StudyPlanResponse)
def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取学习计划详情"""
    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    return plan

@router.put("/task/{task_id}/complete")
def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """完成任务"""
    task = db.query(StudyTask).join(StudyPlan).filter(
        StudyTask.id == task_id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.status = "completed"
    task.completed_date = datetime.utcnow()
    db.commit()
    return {"message": "Task completed successfully"}

@router.put("/task/{task_id}/skip")
def skip_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """跳过任务"""
    task = db.query(StudyTask).join(StudyPlan).filter(
        StudyTask.id == task_id,
        StudyPlan.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.status = "skipped"
    db.commit()
    return {"message": "Task skipped successfully"} 