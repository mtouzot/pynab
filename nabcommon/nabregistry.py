from typing import Callable, Awaitable, Dict

from .typing import NabdPacket

NabHandler = Callable[[NabdPacket], Awaitable[None]]


class NabRegistry:
    """
    Registry for packet handlers
    """

    def __init__(self):
        self.__handlers = Dict[str, NabHandler] = {}

    def register(self, packet_type: str):
        """
        Register a handler for a given packet type
        """

        def decorator(fn: NabHandler):
            self.__handlers[packet_type] = fn
            return fn

        return decorator

    def get(self, packet_type: str):
        return self.__handlers.get(packet_type)
