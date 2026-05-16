from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, get_current_user, require_role
from modules.moderation.presentation.schemas import (
    ModerationEventDetail,
    ModerationEventListItem,
    ModerationQueueItem,
    ModerationStatsResponse,
    ReviewActionRequest,
)

router = APIRouter()

_reviewer = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MODERATOR)
_analyst = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.ANALYST)


@router.get(
    "/events",
    response_model=PaginatedResponse[ModerationEventListItem],
    summary="List moderation events",
)
async def list_events(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[ModerationEventListItem]:
    raise NotImplementedError


@router.get(
    "/events/{event_id}",
    response_model=StandardResponse[ModerationEventDetail],
    summary="Get moderation event detail",
)
async def get_event(
    event_id: UUID,
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModerationEventDetail]:
    raise NotImplementedError


@router.post(
    "/events/{event_id}/review",
    response_model=StandardResponse[ModerationEventDetail],
    summary="Submit review decision",
)
async def review_event(
    event_id: UUID,
    body: ReviewActionRequest,
    current_user: AuthenticatedUser = Depends(_reviewer),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModerationEventDetail]:
    raise NotImplementedError


@router.get(
    "/queue",
    response_model=PaginatedResponse[ModerationQueueItem],
    summary="Pending review queue",
)
async def get_queue(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(_reviewer),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[ModerationQueueItem]:
    raise NotImplementedError


@router.get(
    "/stats",
    response_model=StandardResponse[ModerationStatsResponse],
    summary="Moderation statistics",
)
async def get_stats(
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModerationStatsResponse]:
    raise NotImplementedError
