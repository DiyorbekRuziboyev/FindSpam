from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, require_role
from modules.analytics.presentation.schemas import (
    AnalyticsSnapshotResponse,
    CategoryBreakdownItem,
    DashboardSummaryResponse,
    LanguageBreakdownItem,
    TrendResponse,
)

router = APIRouter()

_analyst = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.ANALYST)


@router.get(
    "/dashboard",
    response_model=StandardResponse[DashboardSummaryResponse],
    summary="Real-time dashboard summary",
)
async def get_dashboard(
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[DashboardSummaryResponse]:
    raise NotImplementedError


@router.get(
    "/trends",
    response_model=StandardResponse[TrendResponse],
    summary="Spam trend data for a given period",
)
async def get_trends(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[TrendResponse]:
    raise NotImplementedError


@router.get(
    "/snapshots",
    response_model=PaginatedResponse[AnalyticsSnapshotResponse],
    summary="Historical daily analytics snapshots",
)
async def list_snapshots(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[AnalyticsSnapshotResponse]:
    raise NotImplementedError


@router.get(
    "/breakdown/languages",
    response_model=StandardResponse[list[LanguageBreakdownItem]],
    summary="Spam breakdown by language",
)
async def language_breakdown(
    days: int = Query(default=30, ge=1, le=365),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[list[LanguageBreakdownItem]]:
    raise NotImplementedError


@router.get(
    "/breakdown/categories",
    response_model=StandardResponse[list[CategoryBreakdownItem]],
    summary="Spam breakdown by category",
)
async def category_breakdown(
    days: int = Query(default=30, ge=1, le=365),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[list[CategoryBreakdownItem]]:
    raise NotImplementedError
