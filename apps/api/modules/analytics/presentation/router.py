from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats() -> None:
    pass


@router.get("/spam-trends")
async def get_spam_trends() -> None:
    pass


@router.get("/threat-heatmap")
async def get_threat_heatmap() -> None:
    pass


@router.get("/group-leaderboard")
async def get_group_leaderboard() -> None:
    pass


@router.get("/category-distribution")
async def get_category_distribution() -> None:
    pass
