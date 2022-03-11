def end_zeros(num: int) -> int:
    # your code here
    lv_count = 0

    lt = str(num)
    for ch in lt[::-1]:
        if ch == "0":
            lv_count += 1
        else:
            return lv_count

    return lv_count


if __name__ == "__main__":
    print("Example:")
    print(end_zeros(0))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert end_zeros(0) == 1
    assert end_zeros(1) == 0
    assert end_zeros(10) == 1
    assert end_zeros(101) == 0
    assert end_zeros(245) == 0
    assert end_zeros(100100) == 2
    print("Coding complete? Click 'Check' to earn cool rewards!")
