from nonebot.default_config import *

SUPERUSERS = {3341659982}
COMMAND_START = {'', '/'}
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event

# 捕获所有消息
message_handler = on_message()

@message_handler.handle()
async def handle_message(bot: Bot, event: Event):
    msg = event.get_message().strip()
    if msg.startswith("你好"):
        await message_handler.finish("你好！")
