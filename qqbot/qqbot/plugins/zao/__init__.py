from nonebot import require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger

__plugin_meta__ = PluginMetadata(
    name="早",
    description="每天 0:00 准时向每个群聊发送消息“早”",
    usage="自动发送",
)

scheduler = require("nonebot_plugin_apscheduler").scheduler

blacklist = []

@scheduler.scheduled_job("cron", hour=0, minute=0)
async def send_daily_greeting():
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