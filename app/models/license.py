from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class License(BaseModel):
    license_id: Optional[str] = None
    product_name: str
    description: Optional[str] = None
    price: float
    supported_platforms: Optional[str] = None
    supported_launchers: Optional[str] = None
    recommendations: Optional[str] = None
    product_version: Optional[str] = None
    has_spoofer: bool = False
    language: Optional[str] = None
    create_at: Optional[str] = None
    update_at: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True
    image_url: Optional[str] = None
    category: Optional[str] = None 