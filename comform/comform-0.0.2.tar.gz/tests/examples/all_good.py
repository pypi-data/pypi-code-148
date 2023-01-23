# -- Real Code ----------------------------------------------------------------------- #

# In arithmetic and algebra, the cube of a number n is its third power, that is, the
# result of multiplying three instances of n together -
# `https://en.wikipedia.org/wiki/Cube_(algebra)`
def cube_sum(
    start,  # start summing from here
    stop,   # stop summing here
):
    """Sum of the squares from `start` to `stop` inclusive."""
    # a much better method exists in the form of a algebraic formula which, for example,
    # students may learn in the first year of a Further Mathematics A level
    return sum(y**3 for y in range(start, stop + 1))


def _sum_first_n_cubes(n):
    return (n * (n + 1)) ** 2 // 4


def better_cube_sum(start, stop):
    return _sum_first_n_cubes(stop) - _sum_first_n_cubes(start - 1)


# -- Test script --------------------------------------------------------------------- #


def main():
    n, m = 11, 15
    assert cube_sum(n, m) == better_cube_sum(n, m)
    print("success!")


if __name__ == "__main__":
    main()
