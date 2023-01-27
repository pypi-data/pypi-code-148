def pattern_triangle(n):
    for i in range(n):
        for j in range(i+1):
            print("*", end=" ")
        print()

def pattern_number_triangle(n):
    for i in range(n):
        for j in range(i+1):
            print(j+1, end=" ")
        print()

def pattern_number_triangle2(n):
    for i in range(n):
        for j in range(i+1):
            print(i+1, end=" ")
        print()

def pattern_square(n):
    for i in range(n):
        for j in range(n):
            print("*", end=" ")
        print()

def pattern_rectangle(n, m):
    for i in range(n):
        for j in range(m):
            print("*", end=" ")
        print()

def pattern_right_triangle(n):
    for i in range(n):
        for j in range(i+1):
            print("*", end=" ")
        print()