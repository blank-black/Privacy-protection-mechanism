import numpy as np
import matplotlib.pyplot as plt
T = 3600
k0=0.07
k1=0.05
k2=0.1


def ebbinghaus1(x):
	y1 = 1/(k0*x**0.5+1)
	y2 = 1/(k0*(x-1)**0.5+1)
	return y1/y2

def ebbinghaus2(x):
	y1 = 1/(k1*x**0.3+1)
	y2 = 1/(k1*(x-1)**0.3+1)
	return y1/y2

def ebbinghaus3(x):
	y1 = 1/(k2*x+1)
	y2 = 1/(k2*(x-1)+1)
	return y1/y2


if __name__ == '__main__':
	source1=100
	source2=100
	source3=100
	x1=[]
	x1.append(0)
	y1=[]
	y1.append(source1)
	x2=[]
	x2.append(0)
	y2=[]
	y2.append(source2)
	x3=[]
	x3.append(0)
	y3=[]
	y3.append(source3)

	for t in range(T * 24 * 30):
		if t > 0 and t % T == 0:
			x1.append(t/T)
			source1=source1*ebbinghaus1(t/T)
			y1.append(source1)
			print('1',source1)
			x2.append(t/T)
			source2=source2*ebbinghaus2(t/T)
			y2.append(source2)
			print('2',source2)
			x3.append(t/T)
			source3=source3*ebbinghaus3(t/T)
			y3.append(source3)
			print('3',source3)

plt.scatter(x1, y1, alpha=0.6,c='r',marker='.')
plt.scatter(x2, y2, alpha=0.6,c='g',marker='.')
plt.scatter(x3, y3, alpha=0.6,c='b',marker='.')
plt.legend(['l1','l2','l3'])
plt.xlabel('time/h')
plt.ylabel('influence/%')

plt.show()