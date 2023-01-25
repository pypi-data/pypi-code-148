class example(object):
    def add_one(number):

        print('This is a print from my package. number = ',number)
        return number + 1


if __name__ == '__main__':
    obj = example.add_one(3)
