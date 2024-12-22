from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
import random
import datetime
import json
import os

# 触发关键词
trigger_keyword = "waifu"

# 定义消息触发器
trigger = on_message()

# 数据文件路径，用于保存每日结果
DATA_FILE = "daily_results.json"

def load_daily_results():
    """加载保存的每日结果数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_daily_results(data):
    """保存每日结果数据到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def reset_daily_results():
    """重置每日结果（清空当天的抽取记录）"""
    save_daily_results({"last_reset_date": datetime.date.today().isoformat()})

@trigger.handle()
async def handle_waifu(bot: Bot, event: Event):
    """
    群聊触发“waifu”关键词时，随机为用户选择一位“群老婆”。
    每天的抽取记录独立，不同天可以重复抽中相同成员。
    """
    # 获取当天日期
    today = datetime.date.today()
    # 加载每日数据
    daily_results = load_daily_results()

    # 检查是否需要重置数据（跨天）
    last_reset_date = daily_results.get("last_reset_date")
    if last_reset_date != today.isoformat():
        reset_daily_results()
        daily_results = {"last_reset_date": today.isoformat()}

    # 获取消息内容并去掉多余空白
    msg = str(event.get_message()).strip()

    # 如果消息是触发关键词
    if msg.lower() == trigger_keyword:
        group_id = event.group_id if hasattr(event, "group_id") else None
        user_id = event.get_user_id()
        message_id = event.message_id

        # 检查是否在群聊中触发
        if group_id:
            # 获取群聊对应的结果记录
            group_results = daily_results.setdefault(str(group_id), {})
            
            # 如果用户已经抽过，返回结果
            if user_id in group_results:
                selected_member = group_results[user_id]
                name = selected_member.get("nickname") or selected_member.get("card") or str(selected_member.get("user_id"))
                avatar = f"https://q1.qlogo.cn/g?b=qq&nk={selected_member.get('user_id')}&s=640"

                reply = (MessageSegment.text(f"你今日的群老婆是：{name}\n") +
                          MessageSegment.image(avatar) +
                          MessageSegment.reply(message_id))
                await trigger.finish(reply)

            # 获取群成员列表
            members = await bot.get_group_member_list(group_id=group_id)

            if members:
                # 随机选择一名成员
                selected_member = random.choice(members)

                # 记录结果
                group_results[user_id] = {
                    "user_id": selected_member.get("user_id"),
                    "nickname": selected_member.get("nickname"),
                    "card": selected_member.get("card")
                }
                save_daily_results(daily_results)

                # 构造回复消息
                name = selected_member.get("nickname") or selected_member.get("card") or str(selected_member.get("user_id"))
                avatar = f"https://q1.qlogo.cn/g?b=qq&nk={selected_member.get('user_id')}&s=640"

                reply = (MessageSegment.text(f"你今日的群老婆是：{name}\n") +
                         MessageSegment.image(avatar) +
                         MessageSegment.reply(message_id))
                await trigger.finish(reply)
            else:
                # 如果无法获取群成员列表
                await trigger.finish("无法获取群成员列表。")
        else:
            # 如果不是在群聊中触发
            await trigger.finish("此命令仅在群聊中可用。")
