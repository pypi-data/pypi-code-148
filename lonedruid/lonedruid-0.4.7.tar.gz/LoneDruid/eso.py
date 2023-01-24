def power_find(n: int) -> list[int]:
    """Convert an integer into a list of powers of 2.

    Args:
        n (int): Integer to convert

    Returns:
        list[int]: List of powers
    """
    result = [] # * Create an empty list
    binary = bin(n)[:1:-1] # * Loop through the binary of representation of the number backwards but without the ``0b`` prefix
    for x in range(len(binary)): 
        if int(binary[x]):
            result.append(x) # * Append the powers of 2 to result list
    return result

def int_to_eso(n: int, eso_num: bool = True, eso_oper: bool = True):
    if n<0:
        sign='-'
        n=abs(n)
    else:
        sign=''
    """Convert an integer into a esoteric implementation of itself

    Args:
        n (int): Positive only integer that is going to be converted to an esoteric monster

    Returns:
        str: Esoteric implementation of the number {n}
    """
    # * int() = 0
    # * ~int() == -1 ->
    # * -~int() = 1
    powers = power_find(n=n) # * Create a list with all the powers of 2 that are needed to get the number
    buffer = [] # * Create an empty list
    for power in powers:
        if eso_num: # * -~int();
            if eso_oper: # * .__add__ , .__pow__
                if power == 0: # * Use int() instead of -~int() for 0 power (even/odd number)
                    buffer.append(f"(-~int().__add__(-~int())).__pow__(int())")
                else:
                    buffer.append(f"((-~int().__add__(-~int())).__pow__(-~int(){''.join([f'.__add__(-~int())' for _ in range(power-1)])}))")
            else: # * + , **
                buffer.append(f"(-~int()+-~int())**(-~int(){''.join([f'+-~int()' for _ in range(power-1)])})")
        else: # * 2 , {pow}
            if eso_oper:
                buffer.append(f"((2).__pow__({power}))")
            else:
                buffer.append(f"(2**{power})")
    if eso_oper:
        monster = buffer[0]
        for i in buffer[1:]:
            monster +=f".__add__({i})"
    else:
        monster = buffer[0]
        for i in buffer[1:]:
            monster +=f"|({i})"
    return f"{sign}({monster})"
        
                
                
            

def multieso(nums: list[int], path: str = '', eso_num: bool = True, eso_oper: bool = True):
    """Create a file with multiple esoteric monsters inside a list

    Args:   
        nums (list[int]): List of integers to convert
        path (str, optional): Path to output file. Defaults to local 'StuffToEsoOutput.py'.
    """
    output = (f"[{', '.join([int_to_eso(num, eso_num=eso_num, eso_oper=eso_oper) for num in nums])}]")
    if path == '':
        return output
    else:
        with open(path, 'w') as f: # * To create a file and write `[` to it (start a list)
            f.write(f"{output} # type: ignore")