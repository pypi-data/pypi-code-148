class example():
    def __init__(self,number):
        print('example test')
        self.param=self.add_one(number)


    def get_param(self):
        return self.param

    def add_one(self,number):
        # print('This is a print from my package. number = ',number)
        res = number + 1
        return res

if __name__ == '__main__':
    pass
    #obj = example(number=None)
