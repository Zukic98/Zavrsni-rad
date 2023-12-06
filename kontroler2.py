# Demonstrating use of matplotlib.patches.Circle() function
# to plot a colored Circle

import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt

figure, axes = plt.subplots()
Drawing_colored_circle = plt.Circle((0.6, 0.6), 0.2)
#plt.text(0.6, 0.7, "This is a Circle1\Yeah")
Drawing_colored_circle2 = plt.Circle((2, 2), 1)
#plt.text(2, 2.5, "This is a Circle2\nYeah")

plt.xlim(0,100)
plt.ylim(0,100)

axes.set_aspect(1)
axes.add_artist(Drawing_colored_circle)
axes.add_artist(Drawing_colored_circle2)
plt.title('Colored Circle')
plt.show()
