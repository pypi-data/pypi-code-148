class MultTable(object):
    def __init__(self):
        self.types = [int,float]

    def single_table(self, number):
        '''

        :param number: Accepts a number
        :return: list
        '''
        result_list = []
        for i in range(1, 11):
            result_list.append(f'{number} x {i} = {self.multiplier(number, i)}')
        return result_list

    def multiplier(self, num1, num2):
        '''

        :param num1: Accepts a number
        :param num2: Accepts a number
        :return: multiplied result by passing to evaluate function
        '''
        if type(num1) not in self.types or type(num2) not in self.types:
            raise 'Not a valid input. Please enter int or float'
        result = eval(f'{num1} * {num2}')
        return result

    def multiple_tables(self, num_list):
        '''

        :param num_list: takes a list of numbers as input
        :return: list
        '''
        multiple_lists = []
        #  STill in progress so wait
        for i in range(1, len(num_list)+1):
            multiple_lists.append(self.single_table(num_list[i-1]))
        return multiple_lists


# use main method and call function to test for now
# test cases are pending

if __name__ == '__main__':
    a = [7,8,9,2.5]
    x = MultTable().multiple_tables(a)
    # x= MultTable().single_table(9147483650)
    print(x)