from discordapi.gateway import DiscordGateway
import logging
import time

logger = logging.getLogger("NicoBot")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

logger.addHandler(ch)

gw = DiscordGateway("NzY5OTgxODMyMDA2NTk4NzE4.X5W7dg.wRjIlSMRHP6bjf77Jr2pyGKcDso")

gw.connect()

try:
    while True:
        time.sleep(1)
finally:
    gw.disconnect()
