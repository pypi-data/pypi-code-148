
def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp


def pivot(arr, start, end):
    pivot = end
    idx = end - 1

    while idx >= start:
        if arr[idx] > arr[pivot]:
            swap(arr, idx, pivot-1)
            swap(arr, pivot, pivot-1)
            pivot = pivot - 1
        idx -= 1

    return pivot


def quick_sort_r(arr, start, end):
    if start >= end:
        return
    p = pivot(arr, start, end)
    quick_sort_r(arr, start, p-1)
    quick_sort_r(arr, p+1, end)


def quick_sort(arr):
    quick_sort_r(arr, 0, len(arr)-1)


def quick_select_r(arr, start, end, kth):
    p = pivot(arr, start, end)
    if p == kth:
        return arr[p]
    elif p > kth:
        return quick_select_r(arr, start, p - 1, kth)
    else:
        return quick_select_r(arr, p + 1, end, kth)


def quick_select(arr, k):
    return quick_select_r(arr, 0, len(arr) - 1, len(arr) - k)


if __name__ == '__main__':
    arr = [3, 2, 1, 5, 6, 4]
    quick_sort(arr)

    print(arr)

    arr1 = [3, 2, 1, 5, 6, 4]

    print(quick_select(arr1, 2))
