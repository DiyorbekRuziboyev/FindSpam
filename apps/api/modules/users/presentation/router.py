from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_users() -> None:
    pass


@router.get("/{user_id}")
async def get_user(user_id: str) -> None:
    pass


@router.patch("/{user_id}")
async def update_user(user_id: str) -> None:
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: str) -> None:
    pass
