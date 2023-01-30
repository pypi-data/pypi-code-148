import datetime
from typing import Dict
from ayaka import AyakaCat, AyakaConfig

cat = AyakaCat("时区助手")
cat.help = """时区助手
- tz_add <name> <timezone> 添加一条时区转换，东八区为8，西八区为-8，例如
    tz_add 北京 8
    tz_add 伦敦 0
    tz_add 洛杉矶 -8
- tz <name> 返回name对应时区的时间，例如 
    tz 北京
- tz <number> 返回对应时区的时间，例如 
    tz 8
- tz_list 查看所有的时区转换
"""


class Config(AyakaConfig):
    __config_name__ = cat.name
    data: Dict[str, int] = {}


config = Config()


@cat.on_cmd(cmds="tz_add")
async def tz_add():
    try:
        name = str(cat.args[0])
        timezone = int(cat.args[1])
    except:
        await cat.send_help()
        return

    timezone = (timezone+8) % 24 - 8

    config.data[name] = timezone
    config.save()

    await cat.send("添加成功："+get_info(name, timezone))


def get_info(name, timezone):
    if timezone == 0:
        timezone = "零时区"
    elif timezone > 0:
        timezone = f"东{timezone}区"
    else:
        timezone = f"西{-timezone}区"
    return f"[{name}] {timezone}"


@cat.on_cmd(cmds="tz_list")
async def tz_list():
    data = config.data
    items = []
    for name, timezone in data.items():
        items.append(get_info(name, timezone))
    if items:
        await cat.send("\n".join(items))
    else:
        await cat.send("目前没有设置任何时区转换")


@cat.on_cmd(cmds="tz")
async def tz():
    name = str(cat.arg)
    if not name:
        await cat.send_help()
        return

    data = config.data
    if name in data:
        timezone = data[name]
    else:
        try:
            timezone = int(name)
        except:
            await cat.send("不存在可用的时区转换")
            await cat.send_help()
            return

    td = datetime.timedelta(hours=timezone)
    tz = datetime.timezone(td)
    time = datetime.datetime.now(tz=tz)
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    await cat.send(t)
