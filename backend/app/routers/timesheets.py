import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_user
from app.models import Timesheet, User
from app.schemas import TimesheetCreate, TimesheetResponse, TimesheetUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/timesheets", tags=["timesheets"])


@router.post("", response_model=TimesheetResponse)
async def create_timesheet(
    timesheet: TimesheetCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new timesheet entry."""
    db_timesheet = Timesheet(
        user_id=current_user.id,
        project_id=timesheet.project_id,
        date=timesheet.date,
        hours=timesheet.hours,
        note=timesheet.note
    )
    session.add(db_timesheet)
    session.commit()
    session.refresh(db_timesheet)

    logger.info(f"Timesheet created: {db_timesheet.id} by user {current_user.id}")
    return TimesheetResponse.model_validate(db_timesheet)


@router.get("", response_model=List[TimesheetResponse])
async def list_timesheets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all timesheet entries for current user."""
    statement = select(Timesheet).where(Timesheet.user_id == current_user.id)
    timesheets = session.exec(statement).all()

    logger.debug(f"Listed {len(timesheets)} timesheets for user {current_user.id}")
    return [TimesheetResponse.model_validate(t) for t in timesheets]


@router.get("/{timesheet_id}", response_model=TimesheetResponse)
async def get_timesheet(
    timesheet_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific timesheet entry."""
    timesheet = session.get(Timesheet, timesheet_id)

    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet entry not found"
        )

    if timesheet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this timesheet"
        )

    return TimesheetResponse.model_validate(timesheet)


@router.put("/{timesheet_id}", response_model=TimesheetResponse)
async def update_timesheet(
    timesheet_id: int,
    timesheet_data: TimesheetUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a timesheet entry."""
    timesheet = session.get(Timesheet, timesheet_id)

    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet entry not found"
        )

    if timesheet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this timesheet"
        )

    update_data = timesheet_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timesheet, field, value)

    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)

    logger.info(f"Timesheet updated: {timesheet_id}")
    return TimesheetResponse.model_validate(timesheet)


@router.delete("/{timesheet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timesheet(
    timesheet_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a timesheet entry."""
    timesheet = session.get(Timesheet, timesheet_id)

    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timesheet entry not found"
        )

    if timesheet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this timesheet"
        )

    session.delete(timesheet)
    session.commit()

    logger.info(f"Timesheet deleted: {timesheet_id}")
