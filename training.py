import numpy as np
import bqplot
from bqplot import pyplot as plt


def distance(x: tuple, y: tuple) -> float:
    n = len(x)
    if n != len(y):
        return "Tuples are not the same length!"
    else:
        summation = 0.0
        for i in range(n):
            summation += (x[i] - y[i]) ** 2
        return np.sqrt(summation)


a = np.random.rand(100, 2)
b = np.random.rand(100, 2)

a = a * 700

b = b * 30

x_sc = bqplot.LinearScale()
y_sc = bqplot.LinearScale()

ax_x = bqplot.Axis(scale=x_sc, label="X-value")
ax_y = bqplot.Axis(scale=y_sc, label="Y-value", orientation='vertical')

scatters1 = bqplot.Scatter(x=a[:, 0], y=a[:, 1], scales={'x': x_sc, 'y': y_sc}, default_size=5, colors=["navy"], sizes=[10])
scatters2 = bqplot.Scatter(x=b[:, 0], y=b[:, 1], scales={'x': x_sc, 'y': y_sc}, default_size=2, colors=['orange'], sizes=[5])

fig = bqplot.Figure(marks=[scatters1, scatters2], axes=[ax_x, ax_y])

plt.show(fig)
