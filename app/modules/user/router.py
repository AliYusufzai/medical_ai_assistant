from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.modules.user.dto import UserResponse, UserPublicResponse
from app.modules.user.service import UserService

router = APIRouter()


@router.get("/{username}", response_model=UserPublicResponse)
async def get_user_profile(username: str, db: AsyncSession = Depends(get_db)):

    service = UserService(db)  # OOP: instantiate service with injected db
    user = await service.get_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found"
        )

    return user


@router.get("/id/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return user


# @router.patch("/id/{user_id}", response_model=UserResponse)
# async def update_user(
#     user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)
# ):
#     service = UserService(db)
#     user = await service.get_by_id(user_id)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {user_id} not found",
#         )

#     updated_user = await service.update(user, data)
#     return updated_user