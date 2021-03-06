from __future__ import division
from grass_fire import Grassfire
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import turtle

rows = int(turtle.numinput('Rows', 'Enter the desired number of rows: '))
cols = int(turtle.numinput('Columns', 'Enter the desired number of columns: '))
obstProb = 0.3

Grassfire = Grassfire()
grid = Grassfire.random_grid(rows=rows, cols=cols, obstacleProb=obstProb)
colorGrid = Grassfire.color_grid(grid)

fig = plt.figure()
gridPlot = plt.imshow(colorGrid, interpolation='nearest')
ax = gridPlot._axes
ax.grid(visible=True, ls='solid', color='k', lw=1.5)
ax.set_xticklabels([])
ax.set_yticklabels([])

obstText = ax.annotate('', (0.15, 0.01), xycoords='figure fraction')
colText = ax.annotate('', (0.15, 0.04), xycoords='figure fraction')
rowText = ax.annotate('', (0.15, 0.07), xycoords='figure fraction')

def set_axis_properties(rows, cols):
    ax.set_xlim((0, cols))
    ax.set_ylim((rows, 0))
    ax.set_xticks(np.arange(0, cols+1, 1))
    ax.set_yticks(np.arange(0, rows+1, 1))
    gridPlot.set_extent([0, cols, 0, rows])

def update_annotations(rows, cols, obstProb):
    obstText.set_text('Obstacle density: {:.0f}%'.format(obstProb * 100))
    colText.set_text('Rows: {:d}'.format(rows))
    rowText.set_text('Columns: {:d}'.format(cols))

set_axis_properties(rows, cols)
update_annotations(rows, cols, obstProb)

fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

def on_key_press(event):
    global grid, rows, cols, obstProb
    if event.key == 'enter':
        ani._stop()
        exit()
    elif event.key == 'shift':
        Grassfire.set_start_dest(grid)
        Grassfire.reset_grid(grid)
        ani.frame_seq = ani.new_frame_seq()
    elif event.key == 'control':
        grid = Grassfire.random_grid(rows=rows, cols=cols, obstacleProb=obstProb)
        set_axis_properties(rows, cols)
        ani._iter_gen = Grassfire.find_path(grid)
    elif event.key == 'right':
        rows += 1
        update_annotations(rows, cols, obstProb)
    elif event.key == 'left' and rows > 1:
        rows -= 1
        update_annotations(rows, cols, obstProb)
    elif event.key == 'up':
        cols += 1
        update_annotations(rows, cols, obstProb)
    elif event.key == 'down' and cols > 1:
        cols -= 1
        update_annotations(rows, cols, obstProb)
    elif event.key.isdigit():
        obstProb = int(event.key) / 10
        update_annotations(rows, cols, obstProb)
fig.canvas.mpl_connect('key_press_event', on_key_press)

def init_anim():
    Grassfire.reset_grid(grid)
    colorGrid = Grassfire.color_grid(grid)
    gridPlot.set_data(colorGrid)

def update_anim(dummyFrameArgument):
    colorGrid = Grassfire.color_grid(grid)
    gridPlot.set_data(colorGrid)

ani = animation.FuncAnimation(fig, update_anim,
    init_func=init_anim, frames=Grassfire.find_path(grid),
    repeat=True, interval=150)

plt.ion()
plt.show(block=True)


