from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, get_current_user, require_role
from modules.blacklist.presentation.schemas import (
    BlacklistEntryDetail,
    BlacklistEntryListItem,
    BlacklistStatsResponse,
    BulkCheckRequest,
    BulkCheckResultItem,
    CreateBlacklistEntryRequest,
    UpdateBlacklistEntryRequest,
)

router = APIRouter()

_admin = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)


@router.get(
    "/",
    response_model=PaginatedResponse[BlacklistEntryListItem],
    summary="List blacklist/whitelist entries",
)
async def list_entries(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[BlacklistEntryListItem]:
    raise NotImplementedError


@router.post(
    "/",
    response_model=StandardResponse[BlacklistEntryDetail],
    status_code=201,
    summary="Add a blacklist or whitelist entry",
)
async def create_entry(
    body: CreateBlacklistEntryRequest,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[BlacklistEntryDetail]:
    raise NotImplementedError


@router.post(
    "/check",
    response_model=StandardResponse[list[BulkCheckResultItem]],
    summary="Bulk check values against blacklist/whitelist",
)
async def bulk_check(
    body: BulkCheckRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[list[BulkCheckResultItem]]:
    raise NotImplementedError


@router.get(
    "/stats",
    response_model=StandardResponse[BlacklistStatsResponse],
    summary="Blacklist statistics",
)
async def get_stats(
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[BlacklistStatsResponse]:
    raise NotImplementedError


@router.get(
    "/{entry_id}",
    response_model=StandardResponse[BlacklistEntryDetail],
    summary="Get blacklist entry detail",
)
async def get_entry(
    entry_id: UUID,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[BlacklistEntryDetail]:
    raise NotImplementedError


@router.patch(
    "/{entry_id}",
    response_model=StandardResponse[BlacklistEntryDetail],
    summary="Update a blacklist entry",
)
async def update_entry(
    entry_id: UUID,
    body: UpdateBlacklistEntryRequest,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[BlacklistEntryDetail]:
    raise NotImplementedError


@router.delete(
    "/{entry_id}",
    status_code=204,
    summary="Delete a blacklist entry",
)
async def delete_entry(
    entry_id: UUID,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    raise NotImplementedError
