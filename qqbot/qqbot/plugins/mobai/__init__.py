from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.matcher import Matcher
from nonebot.typing import T_State
import random
import datetime

__plugin_meta__ = PluginMetadata(
    name="膜拜",
    description="当群友膜拜是跟着膜拜",
    usage="\%\%、orz、sto",
)

keywords = ["%%", "orz", "sto"]
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message())
    if any(keyword in message for keyword in keywords):
        await trigger.send(MessageSegment.face(297) + MessageSegment.face(297) + MessageSegment.face(297))