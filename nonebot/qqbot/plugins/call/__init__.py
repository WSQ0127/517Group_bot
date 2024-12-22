from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.params import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import logger
import random
import re

keywords = ["丛雨", "丛雨！", "丛雨~"]
message_murasama = ["咦，在叫我吗？怎么啦？", "是在叫我吗！", "叫我有什么事吗?", "主人~有什么吩咐吗？", ]
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message())
    user_id = event.get_user_id()
    logger.info(f"消息来源: {user_id}")
    if msg in keywords:
        await trigger.finish(random.choice(message_murasama))
