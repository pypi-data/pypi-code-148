import os


class DictValidation:
    """
    该类用于验证dict格式数据的结构，保证dict数据中拥有预期的key，防止程序由于访问不存在的key而崩溃。
    使用时请实例化该类的对象，并在构造函数中传入示例数据，后调用该对象的verify_data方法即可开始验证。
    """
    def __init__(self, example: dict):
        self.example = example

    def verify_data(self, data: dict):
        """
        验证初始化函数传入的示例数据结构是否是参数数据的子集。
        :param data: 需要验证的数据。
        :return: 返回两个数据，第一个是验证结果，为布尔型数据，当第一个结果是False时，代表存在缺失的Key，此时第二个数据为缺失key的路径，否则
        第二个返回值为None。
        """
        for key in self.example.keys():
            value = data.get(key)
            if value is None:
                return False, key
            elif type(value) == dict:
                v = DictValidation(self.example.get(key))
                res, path = v.verify_data(value)
                return res, os.path.join(key, path)
        return True, ""
