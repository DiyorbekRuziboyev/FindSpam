from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, get_current_user, require_role
from modules.users.presentation.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserDetail,
    UserListItem,
    UserStatsResponse,
)

router = APIRouter()

_admin = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)


@router.get(
    "/",
    response_model=PaginatedResponse[UserListItem],
    summary="List all users",
)
async def list_users(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    _: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[UserListItem]:
    raise NotImplementedError


@router.post(
    "/",
    response_model=StandardResponse[UserDetail],
    status_code=201,
    summary="Create a new user",
)
async def create_user(
    body: CreateUserRequest,
    _: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[UserDetail]:
    raise NotImplementedError


@router.get(
    "/stats",
    response_model=StandardResponse[UserStatsResponse],
    summary="User statistics",
)
async def get_stats(
    _: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[UserStatsResponse]:
    raise NotImplementedError


@router.get(
    "/{user_id}",
    response_model=StandardResponse[UserDetail],
    summary="Get user by ID",
)
async def get_user(
    user_id: UUID,
    _: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[UserDetail]:
    raise NotImplementedError


@router.patch(
    "/{user_id}",
    response_model=StandardResponse[UserDetail],
    summary="Update user",
)
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    _: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[UserDetail]:
    raise NotImplementedError


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Soft-delete user",
)
async def delete_user(
    user_id: UUID,
    _: AuthenticatedUser = Depends(require_role(UserRole.SUPER_ADMIN)),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    raise NotImplementedError
