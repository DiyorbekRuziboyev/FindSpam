from fastapi import APIRouter

router = APIRouter()


@router.post("/webhook")
async def webhook() -> None:
    pass


@router.get("/groups")
async def list_groups() -> None:
    pass


@router.get("/groups/{group_id}")
async def get_group(group_id: str) -> None:
    pass


@router.patch("/groups/{group_id}/settings")
async def update_group_settings(group_id: str) -> None:
    pass


@router.get("/users/{telegram_id}")
async def get_telegram_user(telegram_id: int) -> None:
    pass
