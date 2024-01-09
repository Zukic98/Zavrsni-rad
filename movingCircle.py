import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

def setPenguins():
    fig = plt.figure()
    board = plt.axes(xlim=(0, 800), ylim=(0, 800))

    x = 10
    y = 10
    r = 10

    for p in range(10):
        circle = plt.Circle((x, y), radius=10)

        board.add_patch(circle)
        t = plt.annotate("cpicpi", xy=(x, y), fontsize=5, ha="center")
        annotation = plt.annotate("", xytext=(x, y), xy=(x+10, y+10), arrowprops=dict(facecolor='r', edgecolor='r', headwidth=6, headlength=6, width=0.1))

        plt.draw()
        plt.pause(0.2)
        circle.remove()
        annotation.remove()
        t.remove()
        x += 10
        y += 10

    plt.show()

setPenguins()