from pydantic import BaseModel
from typing import Optional


class BrandBase(BaseModel):
    name: str

class BrandOut(BrandBase):
    id: int
    class Config:
        from_attributes = True

class BrandCountOut(BaseModel):
    brand: str
    count: int

class BrandMini(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
        

class ProductOut(BaseModel):
    id: int
    title: str
    url : str
    img_url : str
    category: Optional[str]
    price: float
    discounted_price: Optional[float] = None


class ImageContentIn(BaseModel):
    url: str

class ImageContentOut(BaseModel):
    base64: str


class StatusOut(BaseModel):
    status: str


class BrandMini(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True


