from pydantic import BaseModel
from typing import Optional

# --- Brand ---
class BrandBase(BaseModel):
    name: str

class BrandOut(BrandBase):
    id: int
    class Config:
        from_attributes = True

class BrandCountOut(BaseModel):
    brand: str
    count: int

# --- Product ---
class ProductOut(BaseModel):
    id: int
    title: str
    brand: Optional[BrandOut] = None
    category: Optional[str] = None
    price: float
    discounted_price: Optional[float] = None
    class Config:
        from_attributes = True

# --- For /content/ ---
class ImageContentIn(BaseModel):
    url: str

class ImageContentOut(BaseModel):
    base64: str

# --- Status/Message Example ---
class StatusOut(BaseModel):
    status: str
