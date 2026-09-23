import numpy as np

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Pendulum:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.length = 5
        self.mass = 10
        self.theta = np.pi/4
        self.omega = 0
        self.alpha = 0

    def getEndPoint(self):
        endX = self.length * np.cos(self.theta + (-3*np.pi)/2) + self.x
        endY = -self.length * np.sin(self.theta + (-3*np.pi)/2) + self.y
        return endX, endY

class DoublePendulum:
    def __init__(self):
        self.g = 9.81
        self.p1 = Pendulum()
        self.p2 = Pendulum()
        self.p1.theta = np.pi/2
        self.p2.theta = -np.pi/4

    def calculateAlpha(self):
        theta1 = self.p1.theta
        theta2 = self.p2.theta

        omega1 = self.p1.omega
        omega2 = self.p2.omega

        m1 = self.p1.mass
        m2 = self.p2.mass

        l1 = self.p1.length
        l2 = self.p2.length

        delta = theta1 - theta2

        denominator = (
                2 * m1 + m2 - (m2 * np.cos(2 * delta))
        )

        alpha1 = (
                         -self.g * (2 * m1 + m2) * np.sin(theta1)
                         - m2 * self.g * np.sin(theta1 - 2 * theta2)
                         - 2 * np.sin(delta) * m2 * (omega2 ** 2 * l2 + omega1 ** 2 * l1 * np.cos(delta))
                 ) / (l1 * denominator)

        alpha2 = (
                         2 * np.sin(delta) * (
                         omega1 ** 2 * l1 * (m1 + m2)
                         + self.g * (m1 + m2) * np.cos(theta1)
                         + omega2 ** 2 * l2 * m2 * np.cos(delta)
                 )) / (l2 * denominator)

        return alpha1, alpha2
    def step(self, dt):
        alpha1, alpha2 = self.calculateAlpha()

        self.p2.x, self.p2.y = self.p1.getEndPoint()
        self.p1.omega += alpha1 * dt
        self.p2.omega += alpha2 * dt

        self.p1.theta += self.p1.omega * dt
        self.p2.theta += self.p2.omega * dt

    def getEndPoint(self):
        return self.p1.getEndPoint(), self.p2.getEndPoint()

def main():
    dt = 1/10
    pendulumCount = 1

    pendulums = []
    lines = []

    fig, ax = plt.subplots()

    for i in range(pendulumCount):
        pendulums.append(DoublePendulum())
        pendulums[i].p2.theta = i * 0.001
        lines.append([
            ax.plot([], [], 'o-')[0],
            ax.plot([], [], 'o-')[0]
        ])

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal')

    def update(frame):
        for _i in range(pendulumCount):

            pendulums[i].step(dt)

            (x1, y1), (x2, y2) = pendulums[i].getEndPoint()

            lines[i][0].set_data(
                [pendulums[i].p1.x, x1],
                [pendulums[i].p1.y, y1]
            )

            lines[i][1].set_data(
                [x1, x2],
                [y1, y2]
            )

        return [line for pair in lines for line in pair]

    _ani = FuncAnimation(
        fig,
        update,
        interval=15,
        blit=False,
        cache_frame_data=False
    )

    plt.show()

if __name__ == "__main__":
    main()