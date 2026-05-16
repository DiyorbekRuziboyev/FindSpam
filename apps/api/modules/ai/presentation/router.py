from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.db.enums import UserRole
from core.pagination.params import PaginationParams
from core.schemas.response import PaginatedResponse, StandardResponse
from core.security.dependencies import AuthenticatedUser, get_current_user, require_role
from modules.ai.presentation.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    ModelMetricsResponse,
    ModelVersionDetail,
    ModelVersionListItem,
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter()

_admin = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN)
_analyst = require_role(UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.ANALYST)


@router.post(
    "/predict",
    response_model=StandardResponse[PredictionResponse],
    summary="Run AI prediction on a message",
)
async def predict(
    body: PredictionRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[PredictionResponse]:
    raise NotImplementedError


@router.post(
    "/feedback",
    response_model=StandardResponse[FeedbackResponse],
    status_code=201,
    summary="Submit prediction feedback",
)
async def submit_feedback(
    body: FeedbackRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[FeedbackResponse]:
    raise NotImplementedError


@router.get(
    "/models",
    response_model=PaginatedResponse[ModelVersionListItem],
    summary="List AI model versions",
)
async def list_models(
    pagination: PaginationParams = Depends(PaginationParams.as_dependency),
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> PaginatedResponse[ModelVersionListItem]:
    raise NotImplementedError


@router.get(
    "/models/active",
    response_model=StandardResponse[ModelVersionDetail],
    summary="Get currently active model version",
)
async def get_active_model(
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModelVersionDetail]:
    raise NotImplementedError


@router.get(
    "/models/{model_id}",
    response_model=StandardResponse[ModelVersionDetail],
    summary="Get model version detail",
)
async def get_model(
    model_id: UUID,
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModelVersionDetail]:
    raise NotImplementedError


@router.post(
    "/models/{model_id}/activate",
    response_model=StandardResponse[ModelVersionDetail],
    summary="Activate a model version",
)
async def activate_model(
    model_id: UUID,
    current_user: AuthenticatedUser = Depends(_admin),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModelVersionDetail]:
    raise NotImplementedError


@router.get(
    "/metrics",
    response_model=StandardResponse[ModelMetricsResponse],
    summary="AI model performance metrics",
)
async def get_metrics(
    current_user: AuthenticatedUser = Depends(_analyst),
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse[ModelMetricsResponse]:
    raise NotImplementedError
