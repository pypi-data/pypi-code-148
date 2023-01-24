"""
蒙特卡洛树搜索算法的实现
"""

class State:
    """
    状态，蒙特卡洛树的节点

    :param parent: 父节点
    :param prior_probability: 先验概率
    """
    c_product = 
    def __init__(self, parent, prior_probability):
        self.parent = parent
        self.children = []
        self.n = 0
        self.Q = 0
        self.u = 0
        self.prior_probability = prior_probability

    def select(self, factor):
        """
            选择当前情况下的最佳子节点

            :param factor: 参数
            :return: 最佳子节点
        """
        return max(self.children, key=lambda child: child.value(factor))

    def 