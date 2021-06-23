#
# NicoBot is Nicovideo Player bot for Discord, written from the scratch.
# This file is part of NicoBot.
#
# Copyright (C) 2020 Wonjun Jung (KokoseiJ)
#
#    Nicobot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from .const import LIB_NAME
from .util import StoppableThread, SelectableEvent

import json
import time
import random
import select
import logging
from ssl import SSLError
from websocket import WebSocket, WebSocketConnectionClosedException

__all__ = []

logger = logging.getLogger(LIB_NAME)


class WebSocketThread(StoppableThread):
    def __init__(self, url, handler, name):
        super(WebSocketThread, self).__init__()

        self.url = url
        self.sock = None
        self.handler = handler
        self.ready_to_run = SelectableEvent()
        self.name = str(name)

        self.heartbeat_thread = None
        self.init_thread = None

    def run(self):
        self.sock = WebSocket(
            enable_multithread=True,
            skip_utf8_validation=True
        )
        self.run_heartbeat()

        while not self.stop_flag.is_set():
            logger.debug("Connecting to Gateway...")
            try:
                self.sock.connect(self.url)
            except Exception:
                logger.exception("Failed to connect to Gateway.")

            self.run_init_connection()

            self._event_loop()

            logger.warning("Gateway connection is lost!")

            self.ready_to_run.clear()
            try:
                self.cleanup()
            except Exception:
                logger.exception("Exception occured while cleaning up.")

            if not self.stop_flag.is_set():
                time.sleep(random.randint(1, 5))

        logger.debug("Stopping thread...")

        self.heartbeat_thread.stop()

    def run_heartbeat(self):
        logger.debug("Starting heartbeat thread.")
        self.heartbeat_thread = StoppableThread(
            target=self.do_heartbeat,
            name=f"{self.name}_heartbeat"
        )
        self.heartbeat_thread.start()

    def run_init_connection(self):
        logger.debug("Starting init thread.")
        self.init_thread = StoppableThread(
            target=self.init_connection,
            name=f"{self.name}_init"
        )
        self.init_thread.start()

    def _event_loop(self):
        while self.sock.connected:
            rl, _, _ = select.select((self.sock.sock,), (), ())
            if self.sock.sock not in rl:
                continue
            try:
                data = self.sock.recv()
                if not data:
                    continue
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                logger.error(f"Gateway returned invalid JSON data:\n{data}")
            except WebSocketConnectionClosedException:
                break
            except Exception:
                logger.exception(
                    "Exception occured while receiving data from the gateway.")

            try:
                logger.debug("Received " + data)
                self.handler(parsed_data)
            except Exception:
                logger.exception(
                    "Exception occured while running handler function.")

    def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)

        try:
            logger.debug("Sent " + data)
            return self.sock.send(data)
        except SSLError:
            logger.exception("SSLError while sending data! retrying...")
            return self.send(data)

    def is_ready(self):
        return self.ready_to_run.is_set()

    def stop(self, status=1000):
        super(WebSocketThread, self).stop()
        self.sock.close(status=status)

    def init_connection(self):
        raise NotImplementedError()

    def do_heartbeat(self):
        raise NotImplementedError()

    def cleanup(self):
        raise NotImplementedError()