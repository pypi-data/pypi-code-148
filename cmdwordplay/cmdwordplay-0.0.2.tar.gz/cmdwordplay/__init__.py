__version__ = '0.0.1'
import time


def main():
    打印("这是一段示例代码")
    旁白(["你醒了", "在一个洞里", "而你被眼前的场景吓了一跳——白色的骷髅头堆成了山", "但是你得赶紧出去"])
    选择([
        ["爬上去", lambda:旁白(["你发现白骨山的山顶刚好到达洞口", "于是你爬了上去"])],
        ["观察四周", lambda:旁白(["你什么也没发现"])]],
        1)
    旁白(["本以为外面的世界会好一些", "但外面确是一片荒芜"])
    选择([
        ["向前走", ["你向前走去"]],
        ["向后方走", lambda:旁白(["你转头向后方看去"])],
        ["向左走", lambda:旁白(["你向左边走去", "走了一会你遇到了一只狮子", "你s了"])],
        ["向右边走", lambda:旁白(["你向右边走去"])]])
    旁白(["你醒了", "在一个洞里", "而你被眼前的场景吓了一跳——白色的骷髅头堆成了山", "但是你得赶紧出去"])


pass


def printVerbatim(text: str, num: float = 0.15):
    """
    定义一个函数参数有两个text和num限制text只能是字符串num只能是浮点数,num如果不传入默认为0.15
    逐字打印传入的text的每个字,打印间隔为num的值单位为秒
    使用样例:
    1.传入所有参数
        1-1.隐式传参
            printVerbatim("你醒了？",0.1)
        1-1.显式传参
            printVerbatim(text="你醒了？",num=0.1)
    2.不传入num参数,使用默认值
        2-1.隐式传参
            printVerbatim("你醒了？")
        2-1.显式传参
            printVerbatim(text="你醒了？")
    """
    strlist = list(text)  # 将字符串转换为列表 | "Hello" ->  ["H","e","l","l","o"]
    for i in strlist:  # 循环遍历列表将字母依次赋值给i
        # 打印每个字母
        # end='' 是用来设置每次打印结尾的字符,默认为end="\n"及默认换行 设置为end=''则不在结尾添加任何内容也不换行
        # flush=True 强制每次打印刷新输出流,否则无法输出
        print(i, end='', flush=True)
        time.sleep(num)  # 打印完一个字符等待num秒,num默认为0.15
    else:  # 如果循环正常结束(即不是由break结束)则执行下面语句
        print()  # 整句打印完换一行


def described(li: list[str] | str, num: float = 1, sonnum: float = 0.15):
    """
    定义一个函数参数有三个li、num (这个是打印完一句话暂停的事件,不传默认为1)、和sonnum (这个是打印完一个字符暂停的事件不传默认为0.15)
    将列表内的每个元素使用printVerbatim函数进行逐字输出
    使用样例:
    described(["你好","我是哔哩哔哩的一个up主"])
    """
    if type(li) is str:
        li = list(filter(lambda v: len(v) != 0, li.split("\n")))
    for i in li:
        printVerbatim(i, sonnum)
        time.sleep(num)


def select(li: list, num: int | None = None):
    """
    定义一个函数参数有两个li、num (这个是正确的选项不传入默认为空,及任意选项都是正确的,如果不正确则会循环正确则跳出循环)
    li列表内容也是一个列表,内部列表的第一个元素是选项的文字,第二个参数是选择该选项后触发的事件,如果第二个元素是函数则会运行是列表则调用described函数传入该列表
    使用样例:
    select(
        [
            ["向前走",["你看见了一朵花","花是白色的"]],
            ["向后走",["你摔死了"]],
            ["向左走",lambda :print("一个小女孩说:你没事吧?")],
        ]
        )
    """
    described([f"{i+1}.{x[0]}" for i, x in enumerate(li)], 0.75)
    while True:  # 进行死循环
        # 使用列表推导式取得所有选项的文字使用described函数进行打印
        try:
            # 获取输入并转化为数字如果转化失败则进行错误处理打印print("请输入数字序号")
            XD: int = int(input("你选择:"))
            if callable(li[XD-1][1]):  # 如果传入的是函数则运行函数
                li[XD-1][1]()
            elif type(li[XD-1][1]) is list:  # 如果传入的是列表则调用described函数打印
                described(li[XD-1][1])
            if num == None or num == XD:  # 如果select的与正确选项num一致或没有设置正确选项则结束循环
                break
        except Exception as err:
            print("请输入正确的数字序号")
        else:
            described([f"{i+1}.{x[0]}" for i, x in enumerate(li)], 0.75)


打印 = printVerbatim
旁白 = described
选择 = select

if __name__ == "__main__":
    main()
