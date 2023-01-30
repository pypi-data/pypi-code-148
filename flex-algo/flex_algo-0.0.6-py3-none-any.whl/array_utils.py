def two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        expect = target - v
        if seen.get(expect) is not None:
            return [seen[expect], i]
        seen[v] = i
    return [-1, -1]


def max_area(height):
    left = 0
    right = len(height) - 1
    max_res = 0

    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_res = max(max_res, area)

        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1

    return max_res


if __name__ == '__main__':
    res = two_sum([2, 7, 11, 15], 9)
    print(res)

    res2 = two_sum([3, 2, 4], 6)
    print(res2)

    res3 = two_sum([3, 3], 6)
    print(res3)

    max_res = max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(max_res)



