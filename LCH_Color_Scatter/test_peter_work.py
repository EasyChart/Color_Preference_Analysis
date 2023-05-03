from PIL import Image
import csv
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

from sklearn.cluster import MeanShift, estimate_bandwidth

# from plotnine import *
# 3.7以前的python才能用plotnine
from itertools import permutations
from skimage import color


plt.rc('axes', axisbelow=True)

# backgroud color
arr = np.arange(0, 256, 5)
rgb = []
for index_r, i_r in enumerate(arr):
    for index_g, i_g in enumerate(arr):
        for index_b, i_b in enumerate(arr):
            rgb.append([i_r, i_g, i_b])
bcg_color = np.array(rgb)
bcg_color_lab = color.rgb2lab(bcg_color/255)
# arr = np.arange(0, 256, 5)
# rgb = np.array(np.meshgrid(arr, arr, arr)).T.reshape(-1, 3)
# print(rgb)


# color_center
df_centers = pd.read_csv('Solid_Color.csv')
centers = df_centers.to_numpy()
centers_values_rgb = centers[:, 7:]
centers_values_lab = centers[:, 4:7]


# plot==========================

# plot peter's work value ===================

fig2 = plt.figure(figsize=(16, 8))
fig2.subplots_adjust(wspace=-0.5)

ax21 = fig2.add_subplot(121)

# 21
# get location

ax21.scatter(bcg_color_lab[:, 1],
             bcg_color_lab[:, 2], c=bcg_color/255, s=50, alpha=0.01)
ax21.scatter(centers_values_lab[:, 1],
             centers_values_lab[:, 2], c=centers_values_rgb/255, s=200, edgecolors='white', alpha=1)


ax21 = plt.gca()
# ax21.set_xlabel('a*')
# ax21.set_ylabel('b*')
ax21.set_xlim([-110, 110])
# ax21.set_ylim([-100, 100])
font = {'family': 'Times New Roman',
        'style': 'italic',
        'weight': 'bold',
        'size': 22
        }


ax21.text(100, 5, 'a*', fontdict=font)
ax21.text(5, 100, 'b*', fontdict=font)

# 设置上边和右边无边框
ax21.spines['right'].set_color('none')
ax21.spines['top'].set_color('none')
ax21.spines['bottom'].set_position(('data', 0))
ax21.spines['left'].set_position(('data', 0))
ax21.set_aspect('equal')
ax21.grid()

#  22
ax22 = fig2.add_subplot(122)

ax22.text(-10, 50, 'L*', fontdict=font)

temp_x_centers = np.zeros((centers_values_lab.shape[0], 1))

ax22.scatter(temp_x_centers[:, 0], centers_values_lab[:, 0], c=centers_values_rgb/255,
             s=200, edgecolors='white', alpha=1)


# ax22.set_ylabel('L*', fontdict=font, rotation=90)
ax22.set_xlim([-10, 10])
ax22.set_xticks([0])
# ax22.set_xtick_params(axis='x', which='both', top=False, bottom=False)
ax22.set_ylim([-5, 105])
# ax2.set_yticks(range(10, 100, 10))
ax22.set_aspect('equal')
# 设置上边和右边无边框
ax22 = plt.gca()
ax22.spines['right'].set_color('none')
ax22.spines['top'].set_color('none')
# ax22.spines['bottom'].set_color('none')
# ax22.spines['top'].set_color('none')
ax22.spines['left'].set_position(('data', 0))
# ax22.grid()


plt.show()
