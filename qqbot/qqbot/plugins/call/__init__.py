from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.params import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import logger
import random
import re

__plugin_meta__ = PluginMetadata(
    name="丛雨",
    description="当群友发送丛雨时回复，替代test",
    usage="丛雨、丛雨！、丛雨~",
)

keywords = ["丛雨", "丛雨！", "丛雨~"]
message_murasama = ["咦，在叫我吗？怎么啦？", "是在叫我吗！", "叫我有什么事吗?", "主人~有什么吩咐吗？", ]
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message())
    user_id = event.get_user_id()
    if message in keywords:
        await trigger.finish(random.choice(message_murasama))
