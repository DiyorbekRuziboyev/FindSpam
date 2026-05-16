from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.database import get_db_session
from core.security.dependencies import AuthenticatedUser, get_current_user
from modules.auth.application.dtos import LoginCommand, LogoutCommand, RefreshTokenCommand
from modules.auth.application.use_cases.login import LoginUseCase
from modules.auth.application.use_cases.logout import LogoutUseCase
from modules.auth.application.use_cases.refresh_token import RefreshTokenUseCase
from modules.auth.presentation.schemas import (
    AuthTokensResponse,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    UserResponse,
)

router = APIRouter()


def _client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else None


@router.post("/login", response_model=AuthTokensResponse)
async def login(
    body: LoginRequest,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> AuthTokensResponse:
    tokens = await LoginUseCase(session).execute(
        LoginCommand(
            email=body.email,
            password=body.password,
            ip_address=_client_ip(request),
            user_agent=request.headers.get("User-Agent"),
        )
    )
    return AuthTokensResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.post("/refresh", response_model=AuthTokensResponse)
async def refresh_token(
    body: RefreshTokenRequest,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> AuthTokensResponse:
    tokens = await RefreshTokenUseCase(session).execute(
        RefreshTokenCommand(
            refresh_token=body.refresh_token,
            ip_address=_client_ip(request),
            user_agent=request.headers.get("User-Agent"),
        )
    )
    return AuthTokensResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.post("/logout", status_code=204)
async def logout(
    body: LogoutRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    await LogoutUseCase(session).execute(
        LogoutCommand(
            refresh_token=body.refresh_token,
            user_id=current_user.id,
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    from modules.auth.infrastructure.repository import UserRepository
    user = await UserRepository(session).get_active_by_id(current_user.id)
    if user is None:
        from core.exceptions.base import NotFoundError
        raise NotFoundError(message="User not found")
    return UserResponse.model_validate(user)
