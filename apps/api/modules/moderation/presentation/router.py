from fastapi import APIRouter

router = APIRouter()


@router.get("/events")
async def list_events() -> None:
    pass


@router.get("/events/{event_id}")
async def get_event(event_id: str) -> None:
    pass


@router.post("/events/{event_id}/action")
async def execute_action(event_id: str) -> None:
    pass


@router.get("/queue")
async def get_queue() -> None:
    pass
