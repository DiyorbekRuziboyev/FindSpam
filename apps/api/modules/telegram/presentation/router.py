from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, get_current_user, require_role
from modules.telegram.presentation.schemas import (
    BanUserRequest,
    TelegramGroupDetail,
    TelegramGroupListItem,
    TelegramUserDetail,
    TelegramUserListItem,
    TelegramUserStatsResponse,
    UnbanUserRequest,
    UpdateGroupSettingsRequest,
)

router = APIRouter()

_admin = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)
_moderator = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MODERATOR)


@router.get(
    "/groups",
    response_model=PaginatedResponse[TelegramGroupListItem],
    summary="List all monitored Telegram groups",
)
async def list_groups(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[TelegramGroupListItem]:
    raise NotImplementedError


@router.get(
    "/groups/{group_id}",
    response_model=StandardResponse[TelegramGroupDetail],
    summary="Get Telegram group detail",
)
async def get_group(
    group_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramGroupDetail]:
    raise NotImplementedError


@router.patch(
    "/groups/{group_id}/settings",
    response_model=StandardResponse[TelegramGroupDetail],
    summary="Update group moderation settings",
)
async def update_group_settings(
    group_id: UUID,
    body: UpdateGroupSettingsRequest,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramGroupDetail]:
    raise NotImplementedError


@router.get(
    "/users",
    response_model=PaginatedResponse[TelegramUserListItem],
    summary="List tracked Telegram users",
)
async def list_telegram_users(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[TelegramUserListItem]:
    raise NotImplementedError


@router.get(
    "/users/{user_id}",
    response_model=StandardResponse[TelegramUserDetail],
    summary="Get tracked Telegram user detail",
)
async def get_telegram_user(
    user_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramUserDetail]:
    raise NotImplementedError


@router.post(
    "/users/{user_id}/ban",
    response_model=StandardResponse[TelegramUserDetail],
    summary="Ban a Telegram user",
)
async def ban_telegram_user(
    user_id: UUID,
    body: BanUserRequest,
    current_user: AuthenticatedUser = Depends(_moderator),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramUserDetail]:
    raise NotImplementedError


@router.post(
    "/users/{user_id}/unban",
    response_model=StandardResponse[TelegramUserDetail],
    summary="Unban a Telegram user",
)
async def unban_telegram_user(
    user_id: UUID,
    body: UnbanUserRequest,
    current_user: AuthenticatedUser = Depends(_moderator),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramUserDetail]:
    raise NotImplementedError


@router.get(
    "/users/stats",
    response_model=StandardResponse[TelegramUserStatsResponse],
    summary="Telegram user statistics",
)
async def get_user_stats(
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TelegramUserStatsResponse]:
    raise NotImplementedError
