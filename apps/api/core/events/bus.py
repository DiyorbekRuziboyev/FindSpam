import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class DomainEvent:
    event_type: str
    payload: dict[str, Any]


Handler = Callable[[DomainEvent], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._handlers.get(event.event_type, [])
        if handlers:
            await asyncio.gather(
                *(handler(event) for handler in handlers),
                return_exceptions=True,
            )


event_bus = EventBus()
