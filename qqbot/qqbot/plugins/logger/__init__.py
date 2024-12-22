from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.params import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import logger
import random
import re

trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    message = str(event.get_message())
    user_id = event.get_user_id()
    logger.info(f"消息: {message}")
    logger.info(f"消息来源: {user_id}")
    if message in keywords:
        await trigger.finish(random.choice(message_murasama))
