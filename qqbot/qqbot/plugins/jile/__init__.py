'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.params import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
import re

keywords = ["草", "艹", "操"]
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message())
    if all(char in keywords for char in msg):
        await trigger.finish("急了🤣👉🤳")
'''