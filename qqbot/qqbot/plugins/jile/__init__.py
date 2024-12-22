from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State

keywords = ["草", "艹", "操"]

feature_enabled = False

trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    global feature_enabled
    msg = str(event.get_message()).strip()

    # 开启功能
    if msg == "#急了":
        feature_enabled = True
        await trigger.finish("急了功能已开启！")

    # 关闭功能
    if msg == "#不急":
        feature_enabled = False
        await trigger.finish("急了功能已关闭！")

    # 功能开启时，匹配关键词
    if feature_enabled and any(char in msg for char in keywords):
        await trigger.finish("急了🤣👉🤳")
