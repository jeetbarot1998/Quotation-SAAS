from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class TenantAwareModel:
    """
    Base mixin for all tenant-aware models.
    Any model inheriting this will automatically be scoped to an organization.
    """
    @declared_attr
    def org_id(cls):
        return Column(Integer, ForeignKey("organizations.id"), nullable=False)

    @declared_attr
    def organization(cls):
        return relationship("Organization")