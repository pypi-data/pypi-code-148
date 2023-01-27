from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt


class WaferMapPlot:
    def __init__(self):
        super()

    @staticmethod
    def plot(defect_points: List[Tuple[float, float]]) -> plt.Figure:

        x = np.linspace(-100, 100, 100)
        y = np.linspace(-100, 100, 100)

        X, Y = np.meshgrid(x, y)

        F = X**2 + Y**2 - 100 * 100

        fig, ax = plt.subplots()

        ax.contour(X, Y, F, [0], colors="black")
        ax.set_aspect(1)

        ax.scatter(*zip(*defect_points), s=1, c="black", marker="s")

        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        plt.xlim(-110, 110)
        plt.ylim(-110, 110)

        return fig
