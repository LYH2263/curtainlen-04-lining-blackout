from fastapi import APIRouter, HTTPException
from app.repositories import fabrics as repo
from app.services import estimate_service
router = APIRouter()
@router.get("/fabrics")
def list_fabrics(window_id: int | None = None):
    if window_id is not None:
        return {"items": estimate_service.panels_by_fabric(window_id)}
    return {"items": repo.list_fabrics()}
@router.get("/fabrics/{fid}")
def get_fabric(fid: int):
    r = repo.get_fabric(fid)
    if not r: raise HTTPException(404)
    return r
