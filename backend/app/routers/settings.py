from fastapi import APIRouter
from app.repositories import settings_repo
router = APIRouter()
@router.get("/settings")
def settings(): return settings_repo.get_all()
@router.post("/settings")
def update_settings(body: dict):
    settings_repo.set_many(body)
    return settings_repo.get_all()
