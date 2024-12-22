from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.matcher import Matcher

# 用于存储消息内容的缓存
last_message = "wocdwelkkdoowafd"
message_count = 1

# 触发器
triiger = on_message()

@triiger.handle()
async def repeat_message(bot: Bot, event: Event):
    global last_message, message_count  # 声明全局变量
    message = event.get_message()
    user_id = event.get_user_id()

    # 来自机器人就跳过
    if user_id == bot.self_id:
        return
    
    # 判断是否重复
    if last_message == message:
        message_count += 1
    else:
        message_count = 1
    
    # 是否重复三遍
    if message_count == 3:
        await bot.send(event, message)
    last_message = message