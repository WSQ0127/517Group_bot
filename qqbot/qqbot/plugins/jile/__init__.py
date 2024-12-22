import json
import os
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State

# 数据文件路径
DATA_PATH = "data/jile.json"

# 关键词列表
keywords = ["草", "艹", "操"]

# 读取配置文件
def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 保存配置文件
def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 创建事件触发器
trigger = on_message()

@trigger.handle()
async def handle_keyword(bot: Bot, event: Event, state: T_State):
    group_id = str(event.group_id) if hasattr(event, "group_id") else str(event.user_id)  # 获取群聊ID或用户ID
    message = str(event.get_message()).strip()

    # 加载当前的功能状态
    data = load_data()
    feature_enabled = data.get(group_id, {}).get("feature_enabled", False)

    # 开启功能
    if message == "#急了":
        data[group_id] = {"feature_enabled": True}
        save_data(data)
        await trigger.finish("急了功能已开启！")

    # 关闭功能
    elif message == "#不急":
        data[group_id] = {"feature_enabled": False}
        save_data(data)
        await trigger.finish("急了功能已关闭！")

    # 功能开启时，匹配关键词
    elif feature_enabled and any(keyword in message for keyword in keywords):
        await trigger.finish("急了🤣👉🤳")
