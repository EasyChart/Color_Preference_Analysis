

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import color
from adjustText import adjust_text #https://www.python-graph-gallery.com/web-text-repel-with-matplotlib


plt.rc('axes', axisbelow=True)
plt.rcParams["font.family"] = "Arial"
import matplotlib.pyplot as mpl
mpl.rcParams['font.size'] = 13

# # backgroud color
# arr = np.arange(0, 256, 5)
# rgb = []
# for index_r, i_r in enumerate(arr):
#     for index_g, i_g in enumerate(arr):
#         for index_b, i_b in enumerate(arr):
#             rgb.append([i_r, i_g, i_b])
# bcg_color = np.array(rgb)
# bcg_color_lab = color.rgb2lab(bcg_color/255)
# # arr = np.arange(0, 256, 5)
# # rgb = np.array(np.meshgrid(arr, arr, arr)).T.reshape(-1, 3)
# # print(rgb)


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

#ax21.scatter(bcg_color_lab[:, 1], bcg_color_lab[:, 2], c=bcg_color/255, s=15, alpha=1)
ax21.scatter(centers_values_lab[:, 1],
             centers_values_lab[:, 2], c=centers_values_rgb/255, s=200, edgecolors='k', alpha=1,linewidth=0.5)


# Add name labels ------------------------------------------------
# Only names that start with the letter "C" are added.
# `ax.text()` outputs are appended to the `TEXTS` list. 
# This list is passed to `adjust_text()` to repel the labels and add arrows.
GREY50 = "#7F7F7F"
GREY30 = "#4d4d4d"
TEXTS = []
for i in range(len(centers_values_lab)):
    
        x = centers_values_lab[i,1]
        y = centers_values_lab[i,2]
        text = str(i)
        TEXTS.append(ax21.text(x, y, text, color=GREY30, fontsize=12, fontname="Arial"))


# Adjust text position and add arrows ----------------------------
# 'expand_points' is a tuple with two multipliers by which to expand
# the bounding box of texts when repelling them from points

# 'arrowprops' receives a dictionary with all the properties we want
# for the arrows
adjust_text(
    TEXTS, 
    expand_points=(3,3),
    arrowprops=dict(
        arrowstyle="-", 
        color=GREY50, 
        lw=1
    ),
    ax=ax21
)


ax21 = plt.gca()
# ax21.set_xlabel('a*')
# ax21.set_ylabel('b*')
ax21.set_xlim([-100, 101])
ax21.set_ylim([-99, 99])
font = {'family': 'Arial',
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
             s=200, edgecolors='k', alpha=1,linewidth=0.5)


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
plt.savefig("Figue4.pdf", formate="pdf",bbox_inches='tight')


plt.show()

