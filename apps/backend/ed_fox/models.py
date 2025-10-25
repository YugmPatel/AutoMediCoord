from pydantic import BaseModel
from typing import Optional, Dict, List

class InboundCase(BaseModel):
    case_id: str
    age: int
    sex: str
    condition: str
    eta_min: int
    vitals: Optional[str] = None
    ekg_flag: bool = False
    message: Optional[str] = None  # optional free-text

class CaseStatus(BaseModel):
    case_id: str
    condition: str
    eta_min: int
    status: Dict[str, str]  # cath, lab, pharmacy, bed, notify

# Add typed request/response models here as you implement agents.