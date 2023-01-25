import ddtank
from ddtank.status import Status

class DDTask:
    status_list = []

    def __init__(self):
        pass

    def __add__(self, other: Status) -> bool:
        """
        添加一个角色到任务队列
        :param other: 被添加的角色
        :return: 返回布尔类型变量，代表操作是否成功
        """
        self.status_list += [other]
        return True

    def __sub__(self, other: Status) -> bool:
        """
        从任务队列删除一个角色
        :param other: 被删除的角色
        :return: 返回布尔类型变量，代表操作是否成功
        """
        if other in self.status_list:
            self.status_list.remove(other)
            return True
        return False

    def __repr__(self) -> str:
        return str(self.status_list)

    def perform(self):
        """
        执行任务队列中所有角色的任务
        :return: 无返回值
        """
        for status in self.status_list:
            ddtank.Thread(target=status.task).start()
