from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_audit_logs() -> None:
    pass


@router.get("/{log_id}")
async def get_audit_log(log_id: str) -> None:
    pass
