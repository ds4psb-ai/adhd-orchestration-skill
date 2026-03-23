"""User router — demonstrates endpoint without frontend consumer."""
from fastapi import APIRouter

from ..services.user_service import get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
def read_user(user_id: int):
    return get_user(user_id)
