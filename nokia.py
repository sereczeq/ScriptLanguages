# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):
    prev = A[0]
    err = -1
    lower = -1
    for elem in A:
        # First find one that is not sorted
        if err == -1:
            if prev > elem:
                err = prev
                # Save the elem after the error elem
                lower = elem
                if lower == err:
                    return False
            # keep track of previous elem
            else:
                prev = elem
        # The list is not swappable if any elements are lower than lower, or bigger than lower but smaller than err
        elif elem < lower or lower < elem < err:
            return False
    return True
    # for i in range(1, len(A) + 1):
    #     try:
    #         a = A[i]
    #     except:
    #         print("whops")
    #     b = A[i - 1]
    #     if err == -1:
    #         if a < b:
    #             err = b
    #     elif lower == -1:
    #         if b < err:
    #             lower = b
    #     else:
    #         if b > lower:
    #             bigger = b
    #             if bigger < err:
    #                 print("false")
    #                 break
    print(err)
    print(lower)
    print(bigger)
    print("------------")


def solutiona(S):
    max_sum = 0
    current_sum = 0
    positive = False
    n = len(S)
    for i in range(n):
        item = S[i]
        if item < 0:
            if max_sum < current_sum:
                max_sum = current_sum
            current_sum = 0
        else:
            positive = True
            current_sum += item
    if (current_sum > max_sum):
        max_sum = current_sum
    if (positive):
        return max_sum
    return -1

def solution2(A):
    length = 1
    index = 0
    while A[index] != -1:
        index = A[index]
        length += 1
    return length


arr1 = [1, -1, 1, 1, 4]
arr2 = [-1, 1, -1]
arr3 = [-1, 3, 4, 5]
arr4 = [2, 3, 1, -1]
print(solutiona(arr1))
print(solutiona(arr2))
print(solutiona(arr3))
print(solutiona(arr4))
quit(0)
arr1 = [1, 5, 3, 3, 7]
arr2 = [1, 3, 5, 3, 4]
arr3 = [1, 3, 5]
arr4 = [1, 4, 2, 3, 4]
arr5 = [1, 2, 3, 4, 10, 5, 6, 7, 8]
arr6 = [1, 2, 3, 4, 10, 10, 10, 6, 7]
arr7 = []
for i in range(1, 100_000):
    arr7.append(i)

arr7[4000] = 3
arr7[5454] = 4

print(solution(arr1))
print(solution(arr2))
print(solution(arr3))
print(solution(arr4))
print(solution(arr5))
print(solution(arr6))
print(solution(arr7))

a1 = [1, 2, 3, 4, 5]
a2 = [-1, -2, -3, -4, -5]
a3 = [1, 1, -1, 1, 1]  # slices the same val
a4 = [4, -1, 1, 1, 1, 1]  # one num is the same as slice of 4
a5 = []  # empty
a6 = [-1, 2, 3, 4, -1]  # starts and ends with negative
a7 = [-1, -2, -3, -4, 5, -6, -7]  # only one positive
