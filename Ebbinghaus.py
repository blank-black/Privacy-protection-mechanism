T = 3600
k=0.25


def ebbinghaus(x):
    y1 = 1/(k*x**0.2+1)
    y2 = 1/(k*(x-1)**0.2+1)
    return y1/y2


if __name__ == '__main__':
    source=100

    for t in range(T * 24 * 15):#t服务器时间
        if t > 0 and t % T == 0:
            source=source*ebbinghaus(t/T)
            print(source)


