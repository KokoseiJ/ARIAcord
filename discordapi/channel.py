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

__all__ = ["Channel"]

from .dictobject import DictObject

DEFAULT_KEY = ["id", "type", "guild_id", "position", "permission_overwrites",
               "name", "topic", "nsfw", "last_message_id", "bitrate",
               "user_limit", "rate_limit_per_user", "recipients", "icon",
               "owner_id", "application_id", "parent_id", "last_pin_timestamp",
               "rtc_region", "video_quality_mode"]


class Channel(DictObject):
    def __init__(self, dictobj):
        super(DictObject, self).__init__(dictobj, DEFAULT_KEY)
