from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.license import License, LicenseCreate, LicenseUpdate
from app.crud.license import license_crud

router = APIRouter(prefix="/licenses", tags=["licenses"])

@router.get("/", response_model=List[License])
async def read_licenses(skip: int = 0, limit: int = 10):
    """Get all licenses with pagination"""
    licenses = await license_crud.get_multi(skip=skip, limit=limit)
    return [License(**license) for license in licenses]

@router.post("/", response_model=License)
async def create_license(license_in: LicenseCreate):
    """Create a new license"""
    license_data = await license_crud.create(license_in)
    return License(**license_data)

@router.get("/{license_id}", response_model=License)
async def read_license(license_id: str):
    """Get a specific license by ID"""
    license_data = await license_crud.get(license_id)
    if not license_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    return License(**license_data)

@router.put("/{license_id}", response_model=License)
async def update_license(license_id: str, license_in: LicenseUpdate):
    """Update a license"""
    # Actualizar la licencia
    update_result = await license_crud.update(license_id, license_in)
    if not update_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Obtener la licencia actualizada completa
    license_data = await license_crud.get(license_id)
    if not license_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    return License(**license_data)

@router.delete("/{license_id}")
async def delete_license(license_id: str):
    """Delete a license"""
    success = await license_crud.delete(license_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    return {"message": "License deleted successfully"} 