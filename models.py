from pydantic import BaseModel,Field

from typing import Optional, List 


class CarModel(BaseModel):
    make: str
    model: str
    year: int = Field(...,ge=2005,lt=2024)
    price: float
    engine: Optional[str] = "V4"
    autonomus: bool
    sold: List[str]