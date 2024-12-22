'''
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.matcher import Matcher
from nonebot.params import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
import re

keywords = "help"
keywords_waifu = "功能 今日老婆"
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message())
    if all(char in keywords for char in msg):
        await trigger.finish(
            """======功能列表======
签到 积分 抽奖 转账
打劫 挖矿 钓鱼 猜拳
猜数字 排行榜 签到状态
领取积分补助 反馈
银行 抢银行 公告板
漂流瓶 邀请码 邀请列表
成语接龙 夺宝 探险
每日一图 打劫记录
今日老婆

以上功能可通过发送[功能 功能名]
可查看功能的使用方法"""
        )
    if all(char in keywords_waifu for char in msg):
        await trigger.finish(
            "Use: waifu 随机娶一位今日群老婆"
        )
'''