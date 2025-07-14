from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LicenseBase(BaseModel):
    product_name: str
    description: Optional[str] = None
    price: float
    supported_platforms: Optional[str] = None
    supported_launchers: Optional[str] = None
    recommendations: Optional[str] = None
    product_version: Optional[str] = None
    has_spoofer: Optional[bool] = False
    language: Optional[str] = None
    stock_quantity: Optional[int] = 0
    is_active: Optional[bool] = True
    image_url: Optional[str] = None
    category: Optional[str] = None

class LicenseCreate(LicenseBase):
    pass

class LicenseUpdate(LicenseBase):
    pass

class LicenseInDBBase(LicenseBase):
    license_id: str
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class License(LicenseInDBBase):
    pass 