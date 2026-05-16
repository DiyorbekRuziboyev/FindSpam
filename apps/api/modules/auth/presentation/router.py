from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login() -> None:
    pass


@router.post("/refresh")
async def refresh_token() -> None:
    pass


@router.post("/logout")
async def logout() -> None:
    pass
