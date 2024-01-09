import matplotlib
matplotlib.use('TKAgg')
#matplotlib.use('TKAgg')
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

fig, ax = plt.subplots()

ax = fig.add_subplot(111)

x = 0
y = 0

circle = plt.Circle((x, y), radius=1)

ax.add_patch(circle)

label = ax.annotate("cpicpi", xy=(x, y), fontsize=30, ha="center")

ax.axis('off')
ax.set_aspect('equal')
ax.autoscale_view()

plt.show()