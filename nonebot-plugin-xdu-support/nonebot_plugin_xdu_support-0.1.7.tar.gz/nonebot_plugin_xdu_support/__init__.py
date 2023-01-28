import nonebot
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent, Message, MessageEvent
from nonebot.typing import T_State
from nonebot.params import ArgStr, CommandArg
from nonebot_plugin_apscheduler import scheduler
from nonebot import require
from libxduauth import EhallSession, SportsSession, XKSession
from builtins import ConnectionError
from pathlib import Path
import asyncio
from datetime import datetime
import os
from .model import check, cron_check, get_sport_record, get_timetable, get_whole_day_course, get_next_course, get_question, des_encrypt, des_descrypt
from .config import Config


# 配置初始项---------------------------------------------------------------

MODLE = {
    "晨午晚检": "Ehall",
    "体育打卡": "Sports",
    "课表提醒": "Ehall",
    "选课操作": "XK",
    "马原测试": "MY"
}

MODEL_NEED = {
    "Ehall": ["学号", "一站式大厅密码"],
    "Sports": ["学号", "体适能密码"],
    "XK": ["学号", "选课密码"],
    "MY": ["随便输入一些吧，反正也不需要补充信息~"]
}

MODEL_RUN_TIME = {
    "晨午晚检": "被动：每天7/13/20点自动打卡，定位在南校区\n主动（晨午晚检查看/查看晨午晚检）：返回本阶段是否已打卡",
    "体育打卡": "被动：每10分钟检测一次，如果您有已上报的正在打卡的记录将会提醒您\n主动（体育打卡查看/查看体育打卡）：返回当前打卡次数信息",
    "课表提醒": "被动：每天早上7点私聊提醒一次今天课表上的课及其位置，每节课前30分钟提醒下节有课\n主动（）：返回当天课表以及此时有没有课，最近的课是在什么时候",
    "选课操作": "暂未编写，但在计划内",
    "马原测试": "被动：无\n主动：返回一道单选或者多选题,可以通过参数决定，无参数默认随机"}

TIME_SCHED = [
    ("8:30", "10:05"),
    ("10:25", "12:00"),
    ("14:00", "15:35"),
    ("15:55", "17:30"),
    ("19:00", "20:35")
]

global_config = nonebot.get_driver().config
xdu_config = Config.parse_obj(global_config.dict())
xdu_support_path = xdu_config.xdu_support_path
superusers = xdu_config.superusers
DES_KEY = xdu_config.des_key

if not DES_KEY:
    DES_KEY = "mdbylcgx"
else:
    if len(DES_KEY) != 8:
        raise KeyError("DES_KEY必须是八位的字符串，请重新设置")

if xdu_support_path == Path():
    xdu_support_path = os.path.expanduser(
        os.path.join('~', '.nonebot_plugin_xdu_support')
    )

XDU_SUPPORT_PATH = os.path.join(xdu_support_path, "user_data")

if not os.path.exists(XDU_SUPPORT_PATH):
    os.makedirs(XDU_SUPPORT_PATH)

for name in MODLE.values():
    if not os.path.exists(os.path.join(XDU_SUPPORT_PATH, f"{name}.txt")):
        f = open(os.path.join(XDU_SUPPORT_PATH, f"{name}.txt"), 'w')
        f.close()

STATE_OK = True
STATE_ERROR = False


# 启动定时器---------------------------------------------------------------

require("nonebot_plugin_apscheduler")

# 注册匹配器----------------------------------------------------------------

add_sub = on_command(
    "xdu功能订阅",
    aliases={
        "xdu服务订阅",
        "xdu添加订阅"},
    priority=4,
    block=True)
cancel_sub = on_command(
    "xdu取消订阅",
    aliases={
        "xdu功能退订",
        "xdu服务退订"},
    priority=4,
    block=True)

chenwuwanjian = on_command(
    "晨午晚检查看",
    priority=6,
    block=True,
    aliases={"查看晨午晚检"})
sport_punch = on_command("体育打卡查看", priority=6, block=False, aliases={"查看体育打卡"})
timetable = on_command("课表查询", priority=6, block=False, aliases={"课表查看"})
update_timetable = on_command("更新课表", priority=6, block=False)
mayuan = on_command("马原", priority=6, block=True)

# 功能订阅-----------------------------------------------------------------


@add_sub.handle()
async def handle(event: PrivateMessageEvent, state: T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg and msg in MODLE.keys():
        state["model"] = msg
    else:
        await asyncio.sleep(1)
        res = "现运行的功能有:\n"
        res += "==========================\n"
        for model in MODLE.keys():
            res += model + "\n"
        res += "==========================\n"
        for model, model_run_time in MODEL_RUN_TIME.items():
            res += f"{model}功能的用法为{model_run_time}\n\n"
        await add_sub.send(res)
        await asyncio.sleep(0.5)


@add_sub.got("model", prompt="请输入想要订阅的功能名称")
async def got_model(event: PrivateMessageEvent, state: T_State, model_: str = ArgStr("model")):
    if model_ in ["取消","算了"]:
        await add_sub.finish("已取消本次操作")
    model = MODLE.get(model_, None)
    state["model"] = model_
    await asyncio.sleep(1)
    if model:
        user_id = str(event.user_id)
        path = Path(XDU_SUPPORT_PATH, f"{model}.txt")
        state["path"] = path
        flag, users = read_data(path)
        if flag:
            users_id = [x[0] for x in users]
            state["user_id"] = user_id
            state["users"] = users
            if user_id in users_id:
                await add_sub.finish(f"您已经订阅{model_}功能哟~")
            else:
                infos = MODEL_NEED[model]
                state["infos"] = infos
                res = "你需要补充的信息有：\n"
                res += "==========================\n"
                for info in infos:
                    res += info + '\n'
                res += "虽然对密码进行了加密处理，但是很遗憾，所有加密都是可逆的，如果不了解bot的主人请谨慎使用插件，谨慎填写密码。可以回复'算了'或者'取消'来取消本次操作，或者在使用完功能后及时取消订阅以免造成损失"
                await add_sub.send(res)
        else:
            await add_sub.finish("读取信息出错了，请及时联系管理员")
    else:
        await add_sub.finish("输入有误，请重新检查您想订阅的功能名称并重试")


@add_sub.got("info", prompt="请以空格对不同信息进行分割，并且不要改变顺序,例如'123456789 abcdefghi'")
async def got_info(event: PrivateMessageEvent, state: T_State, info: str = ArgStr("info")):
    if info in ["取消","算了"]:
        await add_sub.finish("已取消本次操作")
    flag = 0
    await asyncio.sleep(1)
    path = state["path"]
    info = info.split()
    users = state["users"]
    user_id = state["user_id"]
    infos = state["infos"]
    if "一站式大厅密码" in infos:
        try:
            ses = EhallSession(info[0], info[1])
            ses.close()
        except ConnectionError:
            flag = 1
    elif "体适能密码" in infos:
        try:
            ses = SportsSession(info[0], info[1])
            ses.close()
        except ConnectionError:
            flag = 1
    elif "选课密码" in infos:
        try:
            ses = XKSession(info[0], info[1])
            ses.close()
        except ConnectionError:
            flag = 1
    if flag == 0:
        if infos[0] == "随便输入一些吧，反正也不需要补充信息~":
            users.append([user_id, "0", "0"])
        else:
            users.append([user_id] + [info[0], des_encrypt(info[1], DES_KEY).decode()])
        if write_data(path=path, data=users):
            await add_sub.finish(f"成功订阅功能{state['model']}")
        else:
            await add_sub.finish(f"{state['model']}功能订阅失败,请联系管理员")
    else:
        await add_sub.finish("您输入的信息有误请核对后再输入，如果确实无误请联系管理员")


@add_sub.handle()
async def group_handle(event: GroupMessageEvent):
    await asyncio.sleep(1)
    await add_sub.finish("请在聊中处理，本功能不支持群聊")

# 取消订阅---------------------------------------------------------------------------


@cancel_sub.handle()
async def handle(state: T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg and msg in MODLE.keys():
        state["model"] = msg
    else:
        await asyncio.sleep(1)
        res = "现运行的功能有:\n"
        for model in MODLE.keys():
            res += model + "\n"
        await cancel_sub.send(res)


@cancel_sub.got("model", prompt="请输入想要取消订阅的功能名称")
async def got_model(event: MessageEvent, model_: str = ArgStr("model")):
    if model_ in ["取消", "算了"]:
        await cancel_sub.finish("已取消本次操作")

    model = MODLE.get(model_, None)
    await asyncio.sleep(1)
    if model:
        user_id = str(event.user_id)
        path = Path(XDU_SUPPORT_PATH, f"{model}.txt")
        flag, users = read_data(path)
        if flag:
            users_id = [x[0] for x in users]
            if user_id in users_id:
                users.pop(users_id.index(user_id))
                if write_data(path, users):
                    await cancel_sub.finish(f"已经取消{model_}功能的订阅啦！")
                else:
                    await cancel_sub.finish(f"取消{model_}订阅失败，请联系管理员")
            else:
                await cancel_sub.finish(f"您尚未订阅{model_}功能哟~")
        else:
            await cancel_sub.finish("读取信息出错，请及时联系管理员")
    else:
        await cancel_sub.finish("输入有误，请重新检查您想订阅的功能名称并重试")

# 晨午晚检---------------------------------------------------------------------------


@chenwuwanjian.handle()
async def _(event: MessageEvent):
    path = Path(XDU_SUPPORT_PATH, 'Ehall.txt')
    flag, users = read_data(path)
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if flag:
        if user_id in users_id:
            username = users[users_id.index(user_id)][1]
            password = des_descrypt(users[users_id.index(user_id)][2], DES_KEY).decode()
            message = check(username, password)
            await chenwuwanjian.finish(message=f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] {message}')
        else:
            await chenwuwanjian.finish("您没有订阅晨午晚检功能，请先订阅再进行查看",)
    else:
        await chenwuwanjian.finish("获取数据失败，请联系管理员")


# 定时7,14,20
@scheduler.scheduled_job("cron", hour="7,14,20", month="2-7,9-12")
async def run_every_7_hour():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, 'Ehall.txt')
    flag, users = read_data(path)
    if flag:
        for user in users:
            message = check(user[1], des_descrypt(user[2], DES_KEY).decode())
            await bot.send_private_msg(user_id=int(user[0]),
                                       message=f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] {message}')
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='晨午晚检读取数据失败，快维修')

# 体育打卡---------------------------------------------------------------------------


# 定时每10分钟查一次
@scheduler.scheduled_job("cron", minute="*/10", hour="7-22", month="2-7,9-12")
async def run_every_10_minutes():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Sports.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            ses = SportsSession(user[1], user[2])
            flag, res = cron_check(ses, user[1])
            if not flag:
                await asyncio.sleep(1)
                await bot.send_private_msg(user_id=int(user[0]), message=res)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]), message="体育打卡报时任务出错啦，请及时检查")


@sport_punch.handle()
async def _(event: MessageEvent):
    flag, users = read_data(Path(XDU_SUPPORT_PATH, 'Sports.txt'))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        username = users[users_id.index(user_id)][1]
        password = des_descrypt(users[users_id.index(user_id)][2], DES_KEY).decode()
        ses = SportsSession(username, password)
        flag, res = get_sport_record(ses, username)
        await sport_punch.send(res)
        if flag:
            path = Path(XDU_SUPPORT_PATH, "Sports.txt")
            flag, users = read_data(path)
            if flag:
                users_id = [x[0] for x in users]
                users.pop(users_id.index(user_id))
                if write_data(path, users):
                    await sport_punch.finish(f"已经取消体育打卡功能的订阅啦！")
                else:
                    await sport_punch.finish(f"取消体育打卡订阅失败，请联系管理员")
            else:
                await sport_punch.finish("读取信息出错，请及时联系管理员")
        else:
            await sport_punch.finish("打卡还未到次数哦，请继续加油！")
    else:
        await sport_punch.finish("请先订阅体育打卡功能，再进行查询")

# 课表查询---------------------------------------------------------------------------


@update_timetable.handle()
async def _(event: MessageEvent):
    flag, users = read_data(Path(XDU_SUPPORT_PATH, 'Ehall.txt'))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    if user_id in users_id:
        username = users[users_id.index(user_id)][1]
        password = des_descrypt(users[users_id.index(user_id)][2], DES_KEY).decode()

        ses = EhallSession(username, password)
        ses.use_app(4770397878132218)
        get_timetable(ses, username, XDU_SUPPORT_PATH)

        await update_timetable.finish("课表更新成功，启动自动提醒")
    else:
        await update_timetable.finish("请先订阅课表提醒功能，再进行更新")


@timetable.handle()
async def _(event: MessageEvent):
    flag, users = read_data(Path(XDU_SUPPORT_PATH, 'Ehall.txt'))
    users_id = [x[0] for x in users]
    user_id = str(event.user_id)
    message = ""
    if user_id in users_id:
        username = users[users_id.index(user_id)][1]
        password = des_descrypt(users[users_id.index(user_id)][2], DES_KEY).decode()
        if not os.path.exists(
            os.path.join(
                XDU_SUPPORT_PATH,
                f'{username}-remake.json')):
            await timetable.send("未找到本地课表，正在进行在线爬取并储存，请稍等", at_sender=True)
            ses = EhallSession(username, password)
            get_timetable(ses, username, XDU_SUPPORT_PATH)
            await timetable.send("课表更新完成，启动自动提醒，稍后返回数据", at_sender=True)
        message += get_whole_day_course(username, TIME_SCHED, XDU_SUPPORT_PATH)
        await timetable.finish(message)
    else:
        await timetable.finish("请先订阅课表提醒功能，再进行查询")


@scheduler.scheduled_job("cron", hour="8", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_next_course(user[1], XDU_SUPPORT_PATH)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')


@scheduler.scheduled_job("cron", minute="55", hour="9", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_next_course(user[1], XDU_SUPPORT_PATH)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')


@scheduler.scheduled_job("cron", minute="30", hour="13", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_next_course(user[1], XDU_SUPPORT_PATH)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')


@scheduler.scheduled_job("cron", minute="25", hour="15", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_next_course(user[1], XDU_SUPPORT_PATH)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')


@scheduler.scheduled_job("cron", minute="30", hour="18", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_next_course(user[1], XDU_SUPPORT_PATH)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')


@scheduler.scheduled_job("cron", hour="22", month="2-7,9-12")
async def run_at_8():
    bot = nonebot.get_bot()
    path = Path(XDU_SUPPORT_PATH, "Ehall.txt")
    flag, users = read_data(path)
    if flag:
        for user in users:
            if os.path.exists(
                os.path.join(
                    XDU_SUPPORT_PATH,
                    f'{user[1]}-remake.json')):
                message = get_whole_day_course(
                    user[1], TIME_SCHED, XDU_SUPPORT_PATH, 1)
                if message:
                    await bot.send_private_msg(user_id=int(user[0]), message=message)
    else:
        await bot.send_private_msg(user_id=int(superusers[0]),
                                   message='课表提醒读取数据失败，快维修')

# 马原训练---------------------------------------------------------------------------


@mayuan.handle()
async def handle(state: T_State, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if msg:
        if msg[0] == "单选":
            res, ans, _type = get_question(1)
        elif msg[0] == "多选":
            res, ans, _type = get_question(2)
        else:
            res, ans, _type = get_question(3)
    else:
        res, ans, _type = get_question(3)
    state["ans"] = ans
    await mayuan.send(_type + res)


@mayuan.got("user_ans", prompt="请在30秒内作答，格式为小写")
async def _(event: MessageEvent, state: T_State, user_ans: str = ArgStr("user_ans")):
    ans = state["ans"]
    path = Path(XDU_SUPPORT_PATH, "MY.txt")
    (flag, users) = read_data(path)
    # qq_id 答对总个数 答题总个数
    user_id = str(event.user_id)
    users_id = [x[0] for x in users]
    if user_id in users_id:
        current_data = users[users_id.index(user_id)]
        current_all = str(int(current_data[2]) + 1)
        if user_ans.upper() == ans:
            current_correct = str(int(current_data[1]) + 1)
            res_after_ans = "恭喜您回答正确\n"
        else:
            current_correct = current_data[1]
            res_after_ans = f"很遗憾回答错误，正确答案是{ans}\n"
        users[users_id.index(user_id)] = [
            user_id, current_correct, current_all]
        res_after_ans += "****************\n"
        res_after_ans += f"您当前的答题总数为{current_all}\n"
        res_after_ans += f"答对题目总数为{current_correct}\n"
        res_after_ans += f"正确率为{round(int(current_correct)/int(current_all),3)*100}%"
    else:
        current_all = "1"
        if user_ans.upper() == ans:
            current_correct = "1"
            res_after_ans = "恭喜您回答正确\n"
        else:
            current_correct = "0"
            res_after_ans = f"很遗憾回答错误，正确答案是{ans}\n"
        users.append([user_id, current_correct, current_all])
        res_after_ans += "****************\n"
        res_after_ans += f"您当前的答题总数为{current_all}\n"
        res_after_ans += f"答对题目总数为{current_correct}\n"
        res_after_ans += f"正确率为{round(int(current_correct) / int(current_all), 3) * 100}%"
    _ = write_data(path, users)
    await mayuan.finish(res_after_ans)

# 文档操作----------------------------------------------------------------------------


def write_data(path: Path, data: list) -> bool:
    try:
        if data:
            flag = 0
            for info in data:
                if flag == 0:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(' '.join(info))
                    flag = 1
                elif flag == 1:
                    with open(path, 'a', encoding='utf-8') as f:
                        f.write('\n' + (' '.join(info)))
        else:
            with open(path, 'w') as f:
                f.write('')
        return STATE_OK
    except BaseException as e:
        print(e)
        return STATE_ERROR


def read_data(path: Path) -> (bool, list):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.readlines()
        if data:
            infos = [x.split() for x in data]
        else:
            infos = []

        return STATE_OK, infos
    except BaseException as e:
        print(e)
        return STATE_ERROR, []
