from pydantic import BaseModel
from typing import List, Dict


class AddResponse(BaseModel):
    id: int


class StatResponse(BaseModel):
    statistic: Dict[str, int]


class Top5Response(BaseModel):
    timestamp: str
    urls: List[str]
