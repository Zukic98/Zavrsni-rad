import matplotlib
matplotlib.use('TKAgg')
#matplotlib.use('TKAgg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig = plt.figure()
ax = fig.add_subplot(111)

circle1 = patches.Circle((0.3, 0.3), 0.03, fc='r', alpha=0.5)
circle2 = patches.Circle((0.4, 0.3), 0.03, fc='r', alpha=0.5)
button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'Reset', color='g', hovercolor='0.975')
ax.add_patch(circle1)
ax.add_patch(circle2)

def reset(event):
    circle1.set_visible(False)


button.on_clicked(reset)
plt.show()