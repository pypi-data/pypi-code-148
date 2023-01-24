class maths():
    def euclidean_division():
        n1 = int(input('Choose the divisor:\n>>   '))
        n2 = int(input('Choose the denominator:\n>>   '))
        if n2 == 0:
            print("You can't devide a number by 0")
        else:
            result = n1 / n2
            print("Q: ",int(result),"\nR: ",n1 - (int(result) * n2))
