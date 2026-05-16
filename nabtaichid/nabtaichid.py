import datetime
import random
import sys

from nabcommon.nabservice import NabRandomService
from nabcommon.typing import ASREventPacket, RfidEventPacket


class NabTaichid(NabRandomService):
    DAEMON_PIDFILE = "/run/nabtaichid.pid"

    async def get_config(self):
        from . import models

        config = await models.Config.load_async()
        return (config.next_taichi, None, config.taichi_frequency)

    async def update_next(self, next_date, next_args):
        from . import models

        config = await models.Config.load_async()
        config.next_taichi = next_date
        await config.save_async()

    async def perform(self, expiration, args, config):
        packet = (
            '{"type":"command",'
            '"sequence":[{"choreography":"nabtaichid/taichi.chor"}],'
            '"expiration":"' + expiration.isoformat() + '"}\r\n'
        )
        self.writer.write(packet.encode("utf8"))
        await self.writer.drain()

    def compute_random_delta(self, frequency):
        return (256 - frequency) * 60 * (random.uniform(0, 255) + 64) / 128

    async def _handle_asr_forecast(self, packet: ASREventPacket) -> None:
        nlu = packet.get("nlu", {})

        if nlu.get("intent") != "nabtaichid/taichi":
            return

        now = datetime.datetime.now(datetime.timezone.utc)
        expiration = now + datetime.timedelta(minutes=1)
        await self.perform(expiration, None, None)

    async def _handle_rfid_forecast(self, packet: RfidEventPacket) -> None:
        rfid_event = packet.get("event", "removed")
        app = packet.get("app", "")
        if (app == "nabtaichid") and (rfid_event == "detected"):
            now = datetime.datetime.now(datetime.timezone.utc)
            expiration = now + datetime.timedelta(minutes=1)
            await self.perform(expiration, None, None)


if __name__ == "__main__":
    NabTaichid.main(sys.argv[1:])
