from fastapi import APIRouter

router = APIRouter()


@router.get("/domains")
async def list_blacklisted_domains() -> None:
    pass


@router.post("/domains")
async def add_domain() -> None:
    pass


@router.delete("/domains/{domain_id}")
async def remove_domain(domain_id: str) -> None:
    pass


@router.get("/users")
async def list_blacklisted_users() -> None:
    pass


@router.post("/users")
async def add_user() -> None:
    pass


@router.get("/whitelist/domains")
async def list_whitelisted_domains() -> None:
    pass


@router.post("/whitelist/domains")
async def add_whitelist_domain() -> None:
    pass
