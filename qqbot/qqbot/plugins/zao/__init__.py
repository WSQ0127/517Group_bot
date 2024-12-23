'''
import asyncio
from datetime import datetime, timedelta
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger

__plugin_meta__ = PluginMetadata(
    name="早",
    description="每天 0:00 准时向每个群聊发送消息“早”",
    usage="自动发送",
)

blacklist = []

async def send_daily_greeting():
    while True:
        now = datetime.now()
        next_run = (now + timedelta(days=0)).replace(hour=22, minute=2, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()
        logger.info(f"距离下次发送时间还有 {sleep_time} 秒。")
        await asyncio.sleep(sleep_time)

        try:
            bot: Bot = list(Bot.get_bots().values())[0]
            group_list = await bot.call_api("get_group_list")
            for group in group_list:
                group_id = group["group_id"]
                if group_id in blacklist:
                    continue
                await bot.send_group_msg(group_id=group_id, message=MessageSegment.text("早"))
        except Exception as e:
            logger.error(f"发送失败：{e}")

@get_driver().on_startup
async def start_daily_greeting():
    asyncio.create_task(send_daily_greeting())
'''