from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
import re

# 定义消息处理器
mo_mo = on_message()

@mo_mo.handle()
async def handle_mo_mo(bot: Bot, event: Event):
    try:
        logger.debug(f"收到消息内容: {event.raw_message}")

        # 检测关键词 "摸摸"
        if "摸摸" not in event.get_plaintext():
            logger.debug("未匹配关键词 '摸摸'")
            return

        # 提取 @ 的用户QQ号
        at_match = re.search(r"\[CQ:at,qq=(\d+)\]", event.raw_message)
        if not at_match:
            logger.debug("未找到 @ 对象")
            return

        qq_number = at_match.group(1)
        gif_url = f"https://api.52vmy.cn/api/avath/rua?qq={qq_number}"
        logger.debug(f"生成的GIF URL: {gif_url}")

        # 发送图片
        await mo_mo.finish(MessageSegment.image(gif_url))

    except Exception as e:
        logger.error(f"处理消息时发生错误: {e}")