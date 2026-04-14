from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# User schemas
class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    created_at: datetime


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"


# Project schemas
class ProjectCreate(BaseModel):
    """Schema for creating a project."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: int
    user_id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Timesheet schemas
class TimesheetCreate(BaseModel):
    """Schema for creating a timesheet entry."""
    project_id: int
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    hours: float = Field(..., gt=0, le=24)
    note: Optional[str] = Field(None, max_length=500)


class TimesheetUpdate(BaseModel):
    """Schema for updating a timesheet entry."""
    project_id: Optional[int] = None
    date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    hours: Optional[float] = Field(None, gt=0, le=24)
    note: Optional[str] = Field(None, max_length=500)


class TimesheetResponse(BaseModel):
    """Schema for timesheet response."""
    id: int
    user_id: int
    project_id: int
    date: str
    hours: float
    note: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health check schema
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
