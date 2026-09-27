from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import settings_repo
router = APIRouter()

class SettingsPayload(BaseModel):
    default_fullness: Optional[float] = None
    default_lining_hem: Optional[float] = None

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.post("/settings")
def save_settings(body: SettingsPayload):
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if updates.get("default_lining_hem") is not None and updates["default_lining_hem"] < 0:
        raise HTTPException(422, "lining hem must be >= 0")
    if updates.get("default_fullness") is not None and updates["default_fullness"] <= 0:
        raise HTTPException(422, "fullness must be > 0")
    if updates:
        settings_repo.set_many(updates)
    return settings_repo.get_all()
