from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
import random
import datetime
import json
import os

__plugin_meta__ = PluginMetadata(
    name="今日老婆",
    description="每天随机抽取一个群友做老婆",
    usage="waifu",
)

trigger_keyword = "waifu"

trigger = on_message()

DATA_FILE = "data/waifu.json"

def load_daily_results():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_daily_results(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def reset_daily_results():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    save_daily_results({"last_reset_date": datetime.date.today().isoformat()})


@trigger.handle()
async def handle_waifu(bot: Bot, event: Event):

    today = datetime.date.today()
    daily_results = load_daily_results()

    # 重置数据
    last_reset_date = daily_results.get("last_reset_date")
    if last_reset_date != today.isoformat():
        reset_daily_results()
        daily_results = {"last_reset_date": today.isoformat()}

    message = str(event.get_message()).strip()

    if message.lower() == trigger_keyword:
        group_id = event.group_id if hasattr(event, "group_id") else None
        user_id = event.get_user_id()
        message_id = event.message_id

        # 是否在群聊中触发
        if group_id:
            group_results = daily_results.setdefault(str(group_id), {})

            # 如果已经抽过
            if user_id in group_results:
                selected_member = group_results[user_id]
                name = selected_member.get("nickname") or selected_member.get("card") or str(selected_member.get("user_id"))
                avatar = f"https://q1.qlogo.cn/g?b=qq&nk={selected_member.get('user_id')}&s=640"

                reply = (MessageSegment.text(f"你今日的群老婆是：{name}\n") +
                          MessageSegment.image(avatar) +
                          MessageSegment.reply(message_id))
                await trigger.finish(reply)

            members = await bot.get_group_member_list(group_id=group_id)

            if members:
                # 随机选择一名成员
                selected_member = random.choice(members)
                # 记录结果
                group_results[user_id] = {
                    "user_id": selected_member.get("user_id"),
                    "nickname": selected_member.get("nickname"),
                    "card": selected_member.get("card"),
                    "timestamp": datetime.datetime.now().isoformat()
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
                # 无法获取群成员列表
                await trigger.finish("无法获取群成员列表。")
        else:
            # 不是在群聊中触发
            await trigger.finish("此命令仅在群聊中可用。")
