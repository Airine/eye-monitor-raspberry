# _*_ coding: utf-8 _*_

"""
python_visual_animation.py by xianhu
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D
import time

# 解决中文乱码问题
# myfont = fm.FontProperties(fname="/Library/Fonts/Songti.ttc", size=14)
matplotlib.rcParams["axes.unicode_minus"] = False


def simple_plot():
    """
    simple plot
    """
    # 生成画布
    plt.figure(figsize=(8, 6), dpi=80)

    # 打开交互模式
    plt.ion()

    # 循环
    for index in range(200):
        # 清除原有图像
        plt.cla()

        # 设定标题等
        plt.title("Dynamic test")
        plt.grid(True)

        # 生成测试数据
        x = np.linspace(-np.pi + 0.1*index, np.pi+0.1*index, 256, endpoint=True)
        y_cos, y_sin = np.cos(x), np.sin(x)

        # 设置X轴
        plt.xlabel("X")
        plt.xlim(-4 + 0.1*index, 4 + 0.1*index)
        plt.xticks(np.linspace(-4 + 0.1*index, 4+0.1*index, 9, endpoint=True))

        # 设置Y轴
        plt.ylabel("Y")
        plt.ylim(-1.0, 1.0)
        plt.yticks(np.linspace(-1, 1, 9, endpoint=True))

        # 画两条曲线
        plt.plot(x, y_cos, "b--", linewidth=2.0, label="cos")
        plt.plot(x, y_sin, "g-", linewidth=2.0, label="sin")

        # 设置图例位置,loc可以为[upper, lower, left, right, center]
        plt.legend(loc="upper left", shadow=True)

        # 暂停
        plt.pause(0.005)

    # 关闭交互模式
    plt.ioff()

    # 图形显示
    plt.show()
    return
# simple_plot()


def scatter_plot(x, y, func=None):
    """
    scatter plot
    """
    # 打开交互模式    plt.figure(figsize=(8, 6), dpi=80)

    plt.figure(figsize=(9, 9),  dpi=90)
    mngr = plt.get_current_fig_manager()
    mngr.window.wm_geometry("+340+70")
    plt.ion()
    plt.ioff()

    assert len(x) == len(y)
    # 循环
    start_time = time.time()

    flag = -1
    start_time = time.time()
    for index in range(len(x)):
        # 清除原有图像
        plt.cla()

        # 设定标题等
        plt.title("Dynamic test")
        plt.grid(True)
        plt.xlim(0, 12)
        plt.ylim(0, 12)
        scale = 30

        x_ = x[index]*np.ones(1)
        y_ = y[index]*np.ones(1)
        if index < 50:
            if index % 10 == 0:
                flag = -flag
            scale = 500
            x[index] = flag*x[index]
            y[index] = flag*y[index]
        if index == 50:
            ready_time = time.time() - start_time
            print(ready_time)
            func("start")
            # sendCommand("start")

        # 画散点图
        plt.scatter(x[index], y[index], s=scale)

        # 暂停
        plt.pause(0.005)

    # 关闭交互模式
    # plt.ioff()

    # 显示图形
    plt.show()
    return
# scatter_plot()


def three_dimension_scatter():
    """
    3d scatter plot
    """
    # 生成画布
    fig = plt.figure()

    # 打开交互模式
    plt.ion()

    # 循环
    for index in range(50):
        # 清除原有图像
        fig.clf()

        # 设定标题等
        fig.suptitle("Dynamic test")

        # 生成测试数据
        point_count = 200
        x = np.random.random(point_count)
        y = np.random.random(point_count)
        z = np.random.random(point_count)
        color = np.random.random(point_count)
        scale = np.random.random(point_count) * 200

        # 生成画布
        ax = fig.add_subplot(111, projection="3d")

        # 画三维散点图
        ax.scatter(x, y, z, s=scale, c=color, marker=".")

        # 设置坐标轴图标
        ax.set_xlabel("X Label")
        ax.set_ylabel("Y Label")
        ax.set_zlabel("Z Label")

        # 设置坐标轴范围
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)

        # 暂停
        plt.pause(0.01)

    # 关闭交互模式
    plt.ioff()

    # 图形显示
    plt.show()
    return
# three_dimension_scatter()

if __name__ == '__main__':
    ready = 6*np.ones(50, dtype=np.float32)

    x_hori = np.linspace(2, 10, 200,dtype=np.float32)
    x_hore = np.linspace(10, 2, 200,dtype=np.float32)
    x_2 = 2*np.ones(50,dtype=np.float32)
    x_10= 10*np.ones(50,dtype=np.float32)

    y_down = list()
    y_hori = list()
    for i in [10, 8, 6, 4]:
        y_down.append(np.linspace(i, i-2, 50,dtype=np.float32))
        y_hori.append(i*np.ones(200,dtype=np.float32))
    y_hori.append(2*np.ones(200,dtype=np.float32))
    x = np.concatenate((ready, x_hori, x_10, x_hore, x_2,
                        x_hori, x_10, x_hore, x_2,
                        x_hori))
    y = np.concatenate((ready, y_hori[0], y_down[0], y_hori[1], y_down[1],
                        y_hori[2], y_down[2], y_hori[3], y_down[3],
                        y_hori[4]))

    scatter_plot(x,y,print)
