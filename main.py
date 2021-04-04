# Press the green button in the gutter to run the script.
def numerator(x, y) -> int:
    out = 0
    for xi, yi in zip(x, y):
        out += xi * yi
    return out


def denominator(x) -> int:
    out = 0
    for xi in x:
        out += xi * xi
    return out


if __name__ == '__main__':
    x = [1, 2, 3, 4]
    print(type(x) is int)
    x = range(0, 10)
    y = range(10, 30, 2)
    print(numerator(x, y) / denominator(x))




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
