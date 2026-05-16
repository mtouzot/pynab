from .typing import NabdPacket
from .nabregistry import NabRegistry


class NabPacketRouter:
    def __init__(self, registry: NabRegistry):
        self.registry = registry

    async def dispatch(self, packet: NabdPacket):
        if handler := self.registry.get(packet["type"]):
            await handler(packet)
