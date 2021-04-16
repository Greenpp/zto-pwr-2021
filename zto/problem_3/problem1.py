import io
import math

import matplotlib.pyplot as plt
import pandas as pd
from docplex.mp.model import Model


class RandomNumberGenerator:
    def __init__(self, seedVaule=None):
        self.__seed = seedVaule

    def nextInt(self, low, high):
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 = value_0_1 / m
        return low + int(math.floor(value_0_1 * (high - low + 1)))

    def nextFloat(self, low, high):
        low *= 100000
        high *= 100000
        val = self.nextInt(low, high) / 100000.0
        return val


R = RandomNumberGenerator(50)

n = 10

values = []
for i in range(0, n):
    values.append(R.nextInt(-100, 100))

xx = []
for i in range(n):
    xx.append(f'x{i+1}')

df = pd.DataFrame({'values': values}, index=xx)
print(df)

T = R.nextInt(-50 * n, 50 * n)

m = Model(name='Problem sumy podzbioru')

x = []
for i in range(0, n):
    x.append(m.binary_var(name=f'x{i+1}'))

m.minimize(m.abs(T - m.sum(x[i] * values[i] for i in range(0, n))))

m.solve()
print('T: ', T)
m.solve().display()


def Solver(n):
    values = []
    for i in range(0, n):
        values.append(R.nextInt(-100, 100))

    T = R.nextInt(-50 * n, 50 * n)

    m = Model(name='Problem sumy podzbioru')

    x = []
    for i in range(0, n):
        x.append(m.binary_var(name=f'x{i + 1}'))

    m.minimize(m.abs(T - m.sum(x[i] * values[i] for i in range(0, n))))

    out_stream = io.StringIO()
    s = m.solve(log_output=out_stream)

    ex_time = float(out_stream.getvalue().splitlines()[-1].split()[-4])

    return ex_time


numbers = [10, 50, 150, 350, 750, 996]  # 996 - max
timelist = []

for i in numbers:
    timelist.append(Solver(i))

plt.scatter(numbers, timelist)
plt.plot(numbers, timelist)

plt.xlabel('Number of values')
plt.ylabel('Time [s]')
