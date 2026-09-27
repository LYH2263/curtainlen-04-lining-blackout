from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(window_id: int = Query(...), fabric_id: int = Query(...), save: bool = False,
            lining_enabled: bool = False, lining_hem_top: float | None = None,
            lining_hem_bottom: float | None = None):
    return estimate_service.run_estimate(window_id, fabric_id, save, "",
                                         lining_enabled, lining_hem_top, lining_hem_bottom)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(body.window_id, body.fabric_id, body.save, body.note,
                                         body.lining_enabled, body.lining_hem_top, body.lining_hem_bottom)
