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
    user_name = event.get_user_name()
    group_id = event.group_id if hasattr(event, 'group_id') else None
    if group_id:
        group_name = await bot.get_group_info(group_id=group_id)['group_name']
    else:
        group_name = None
    logger.info(f"群聊: {group_name}({group_id})")
    logger.info(f"用户: {user_name}({user_id})")
    logger.info(f"消息: {message}")
