def find_is_prime(num: int) -> bool:
    if num <= 1:
        return False

    prm = 2
    while prm*prm <= num:
        if num % prm == 0:
            return False
        prm += 1

    return True