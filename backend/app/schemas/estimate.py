from typing import Optional

from pydantic import BaseModel

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    lining: bool = False
    lining_hem: Optional[float] = None
