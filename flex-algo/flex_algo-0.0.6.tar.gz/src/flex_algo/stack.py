class Stack:
    def __init__(self):
        self.stack = []

    def is_valid(self, s: str) -> bool:
        parenthese = {'(': ')', '[': ']', '{': '}'}
        for ch in s:
            if parenthese.get(ch) is not None:
                self.stack.append(ch)
            else:
                p = self.stack.pop()
                if parenthese.get(p) != ch:
                    return False

        return len(self.stack) == 0

    def min_remove_to_make_valid(self, s: str) -> str:
        arr_ch = list(s)
        for i in range(len(s)):
            if arr_ch[i] == '(':
                self.stack.append(i)
            elif arr_ch[i] == ')':
                if len(self.stack) == 0:
                    arr_ch[i] = ''
                else:
                    self.stack.pop()

        for i in self.stack:
            arr_ch[i] = ''

        return "".join(arr_ch)


if __name__ == '__main__':
    stack = Stack()
    valid = stack.is_valid('()[]{}')
    print(valid)

    valid_s = stack.min_remove_to_make_valid("lee(t(c)o)de)")
    print(valid_s)
