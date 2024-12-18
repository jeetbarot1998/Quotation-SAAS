from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.dependencies import get_db
from models.organization import Organization
from schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    responses={404: {"description": "Not found"}}
)


@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_organization(
        org_data: OrganizationCreate,
        db: Session = Depends(get_db)
):
    """
    Create a new organization with the following data:
    - **name**: Organization name
    - **subdomain**: Unique subdomain for the organization
    - **email**: Primary contact email
    - **description**: Optional organization description
    """
    try:
        organization = Organization(
            name=org_data.name,
            subdomain=org_data.subdomain.lower(),
            email=org_data.email,
            description=org_data.description
        )
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Organization with this subdomain already exists"
        )


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """
    Retrieve a list of organizations with pagination.
    """
    organizations = db.query(Organization) \
        .offset(skip) \
        .limit(limit) \
        .all()
    return organizations


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
        org_id: str,
        db: Session = Depends(get_db)
):
    """
    Retrieve a specific organization by ID.
    """
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
        org_id: str,
        org_data: OrganizationUpdate,
        db: Session = Depends(get_db)
):
    """
    Update an organization's information.
    Subdomain cannot be updated after creation.
    """
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Update allowed fields
    update_data = org_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)

    try:
        db.commit()
        db.refresh(organization)
        return organization
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Update failed due to constraint violation"
        )


@router.delete("/{org_id}", status_code=204)
async def delete_organization(
        org_id: str,
        db: Session = Depends(get_db)
):
    """
    Delete an organization.
    This will also delete all associated data due to cascade delete.
    """
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    db.delete(organization)
    db.commit()
    return None