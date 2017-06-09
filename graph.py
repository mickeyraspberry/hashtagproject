import time
import threading
import numpy as np
from vkapi import *
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.animation as animation

matplotlib.rcParams['toolbar'] = 'None'

n_groups = 1
fig = plt.figure(num=None, figsize=(16, 8), dpi=80)
fig.canvas.set_window_title('Аналитика хештега в VK.com')


ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 1, 2)

formatter = matplotlib.ticker.NullFormatter()
y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)

ax1.xaxis.set_major_formatter(formatter)
ax2.xaxis.set_major_formatter(formatter)
ax3.xaxis.set_major_formatter(formatter)
ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)
ax3.yaxis.set_major_formatter(formatter)

ax1_object = ('Мужчины', 'Женщины')
ax2_object = ('Люди', 'Группы')
ax3_object = ('Лайки', 'Просмотры')

ax3_per = []
ax1_per = []
ax2_per = []

flag = False


def animate(i):
    global flag
    if not flag:
        return

    plt.subplot(221)
    ax1.clear()
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(y_formatter)
    y_pos = np.arange(len(ax1_per))

    barlist = plt.bar(y_pos, ax1_per, align='center', alpha=0.5)
    barlist[0].set_color('r')
    plt.xticks(y_pos, ax1_object)

    plt.ylabel('Число постов')

    ax2.clear()
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(y_formatter)

    plt.subplot(222)
    barlist = plt.bar(y_pos, ax2_per, align='center', alpha=0.5)
    barlist[0].set_color('r')
    plt.xticks(y_pos, ax2_object)

    plt.ylabel('Число постов')

    ax3.clear()
    ax3.xaxis.set_major_formatter(formatter)
    ax3.yaxis.set_major_formatter(y_formatter)

    plt.subplot(212)

    for i in ax3_per:
        i = i / 1000

    print(ax3_per)

    barlist = plt.bar(y_pos, ax3_per, align='center', alpha=0.5)
    barlist[0].set_color('r')
    plt.xticks(y_pos, ax3_object)

    plt.ylabel('Число пользователей')

    flag = False


def updateInfo(interval, text):
    global ax3_per, ax1_per, ax2_per, flag
    while True:
        ax3_per = getNewsHashTag(text)
        ax1_per = [len(men), len(women)]
        ax2_per = [len(people), len(group)]
        flag = True
        time.sleep(interval)


def startAnim(arg):
    t = threading.Thread(target=updateInfo, args=(1, arg))
    t.daemon = True
    t.start()
    time.sleep(5)
    animate(1)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    mng = plt.get_current_fig_manager()
    bck = plt.get_backend()
    if bck == "TkAgg":
        mng.window.resizable(False, False)
    fig.suptitle('Аналитика хештега в VK.com\nВаш хештег: #' + arg, fontsize=18, fontweight='bold')
    plt.show()