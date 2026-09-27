from pydantic import BaseModel

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    lining_enabled: bool = False
    lining_hem_top: float | None = None
    lining_hem_bottom: float | None = None
