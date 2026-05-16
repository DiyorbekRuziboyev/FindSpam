from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, require_role
from modules.audit.presentation.schemas import (
    AuditLogDetail,
    AuditLogListItem,
    AuditSummaryResponse,
)

router = APIRouter()

_admin = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)


@router.get(
    "/logs",
    response_model=PaginatedResponse[AuditLogListItem],
    summary="List audit log entries",
)
async def list_logs(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[AuditLogListItem]:
    raise NotImplementedError


@router.get(
    "/logs/{log_id}",
    response_model=StandardResponse[AuditLogDetail],
    summary="Get audit log entry detail",
)
async def get_log(
    log_id: UUID,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[AuditLogDetail]:
    raise NotImplementedError


@router.get(
    "/summary",
    response_model=StandardResponse[AuditSummaryResponse],
    summary="Audit log summary and statistics",
)
async def get_summary(
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[AuditSummaryResponse]:
    raise NotImplementedError
