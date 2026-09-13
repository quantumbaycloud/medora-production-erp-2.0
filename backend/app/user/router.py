from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.db.base import get_db
from app.shared.deps import get_current_user
from app.user import service
from app.user.models import User
from app.user.schemas import UserRead, UserUpdate

# Router-level auth dependency, per Section 13 decision: every route in
# this router requires a valid access token. No route-specific auth checks
# needed here since /me actions never require extra permissions.
router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_me(payload: UserUpdate, current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    return service.update_user(db, current_user, payload.name)
