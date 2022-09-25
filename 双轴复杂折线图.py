import numpy as np
import matplotlib.pyplot as plt
# import pyodbc as pd
import matplotlib as mpb
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
# import pylab as pl 使用中文

# --------------------------定义数据映射函数--------------------------
def my_map(map_start, map_end, target, re_start, re_end):
    count_len = len(target)
    i = 0
    map_after = np.zeros(count_len)
    while i < count_len:
        temp_1 = target[i]
        data_after = temp_1 * (map_end - map_start) / (re_end - re_start)
        map_after[i] = data_after
        i = i + 1
    return map_after

# --------------------------定义同类数据放缩--------------------------
# 左轴放缩
# tick_a (85, 105)映射到(7000, 11000)
def shrinks_torque(data):
    data = my_map(1000, 1400, data, 85, 105)
    return data
# tick_b (5, 25)映射到(1000, 6000)
def shrinks_fb(data):
    data = my_map(0, 1200, data, 5, 25)
    return data
# 右轴放缩
# tick_c1 (280, 300)映射到(6000, 11000)
def shrinks_fuel(data):
    data = my_map(600, 900, data, 280, 380)
    return data
# tick_d (10, 60)映射到(1000, 6000)
def shrinks_pow0(data):
    data = my_map(0, 600, data, 10, 60)
    return data

# ---------------------------设置曲线拟合函数---------------------------
# (x轴变量，拟合数据（y轴），拟合顶点)
def fit_polynomial(axis_x, data_fit, num_var):
    coefficient = np.polyfit(axis_x, data_fit, num_var)      # 曲线拟合，返回值为多项式的各项系数
    temp_10 = np.poly1d(coefficient)
    fitting_function = np.poly1d(temp_10)    # 获得（多项式）函数表达式
    print("拟合函数：", fitting_function)
    y_pred = fitting_function(axis_x)
    return fitting_function

# --------------------------曲线连续性数据处理--------------------------
def var_continuity(fitting_function, axis_x, item):
    start = min(axis_x)
    end = max(axis_x)
    temp_vc_x = np.linspace(start, end, item)
    temp_vc_y = fitting_function(temp_vc_x)
    return (temp_vc_x, temp_vc_y)

# ------------------------------数据输入------------------------------
data = np.matrix \
  ([[1200, 89,  3,  298, 11],
    [1600, 93,  4,  301, 15],
    [2000, 95,  7,  294, 19],
    [2400, 97,  7,  286, 24],
    [2800, 103, 8,  286, 30],
    [3200, 103, 10, 289, 34],
    [3600, 102, 11, 293, 38],
    [4000, 99,  12, 291, 41],
    [4400, 104, 14, 303, 47],
    [4800, 104, 16, 320, 52],
    [5200, 103, 18, 331, 56],
    [5600, 99,  20, 347, 58],
    [6000, 95,  21, 363, 60]])

# ------------------------------定义占位------------------------------
(row, column) = data.shape
# 检查点 print(row, column)
rmp = np.zeros(row)
torque = np.zeros(row)
fb_val = np.zeros(row)
fuel = np.zeros(row)
pow0 = np.zeros(row)

# 定义循环，分发数据
temp_c01 = 0
while temp_c01 < row:
    rmp[temp_c01] = data[temp_c01, 0]
    torque[temp_c01] = data[temp_c01, 1]
    fb_val[temp_c01] = data[temp_c01, 2]
    fuel[temp_c01] = data[temp_c01, 3]
    pow0[temp_c01] = data[temp_c01, 4]
    temp_c01 = temp_c01 + 1
# print 检查点

# ---------------------------坐标轴标签定义---------------------------
# 约定y轴显示  左上1：rmp、   左下2：fb_val     右上3：fuel   右下4：pow0
# 定义标签
tick_a = range(85, 106, 5)
tick_b = range(5, 26, 5)
tick_c1 = range(280, 300, 10)
tick_c2 = range(300, 381, 20)
tick_c = np.append(tick_c1, tick_c2)
tick_d = range(10, 61, 5)


# -----------------------数据拟合-----------------------
fun_torque = fit_polynomial(rmp, torque, 9)      # 7, 8, 9, 10, 11 不是这几个数的拟合效果特别差
# fun_fb_val = fit_polynomial(rmp, fb_val, 2)
fun_fuel = fit_polynomial(rmp, fuel, 10)
fun_pow0 = fit_polynomial(rmp, pow0, 10)

# 定义枚举数量
(fit_rmp, fit_torque) = var_continuity(fun_torque, rmp, 90)

# (no_use_1, fit_fb_val) = var_continuity(fun_fb_val, fb_val, 90)
chan_fb_val = fit_rmp * 0.00385 * 59 - 110
(no_use_2, fit_fuel) = var_continuity(fun_fuel, fuel, 90)
(no_use_3, fit_pow0) = var_continuity(fun_pow0, pow0, 90)
chan_pow0 = fit_rmp * 0.00385 * 59 - 110

# -----------------------------执行放缩-----------------------------
mp_torque = shrinks_torque(torque)
temp_a = shrinks_torque(tick_a)
cha_torque = shrinks_torque(fit_torque)

mp_fb_val = shrinks_fb(fb_val)
temp_b = shrinks_fb(tick_b)


mp_fuel = shrinks_fuel(fuel)
temp_c = shrinks_fuel(tick_c)

mp_pow0 = shrinks_pow0(pow0)
temp_d = shrinks_pow0(tick_d)
# 检查点 print(temp_a)

# ------------------------------拼接------------------------------
# 设置实际轴标度
tick_left_n = np.append(temp_b, temp_a)
tick_right_n = np.append(temp_d, temp_c)
# 设置映射轴标度
tick_left = np.append(tick_b, tick_a)
tick_right = np.append(tick_d, tick_c)
print(tick_right)
print(tick_right_n)
# 检查点
# list(tick_left)
# list(tick_right)

# ----------------------------画图主程序----------------------------
plt.figure()
# 创建第一个坐标轴
fig, ax1 = plt.subplots()
# 依据 左y轴 ，画rmp-torque，rmp-fb_val的
ax1.scatter(rmp, mp_torque, color='blue', marker='+', label='torque')
ax1.plot(fit_rmp, cha_torque, color='blue', marker='o', linestyle='solid', linewidth=1, markersize=1, label='torque')
plt.legend(loc='upper left')
ax1.scatter(rmp, mp_fb_val, color='blue', marker='^', label='fb_val')
ax1.plot(fit_rmp, chan_fb_val, color='blue', marker='o', linestyle='dashed', linewidth=1, markersize=1, label='fb_val')
plt.legend(loc='upper left')
# 修改 左y轴标度
plt.yticks(tick_left_n, tick_left, color="blue", rotation=0)
# 添加图例
plt.legend()
# 修改缩放比例S
# mpb.legend(loc=2) # 标注放置位置

# ---------------------------创建第二个坐标轴---------------------------
ax2 = ax1.twinx()
# 依据 右y轴 ，画rmp-torque，rmp-fb_val的
ax2.scatter(rmp, mp_pow0, color='green', marker='*', label='pow0')
ax2.plot(fit_rmp, chan_pow0, color='green', marker='o', linestyle='dashed', linewidth=1, markersize=1, label='fb_val')
plt.legend(loc='upper left')
ax2.scatter(rmp, mp_fuel, color='red', marker='p', label='fuel')
plt.legend(loc='upper left')
# mpb.legend(loc=1) # 标注放置位置
# 修改 右y轴标度
plt.yticks(tick_right_n, tick_right, color="red", rotation=0)
print(mp_fuel)
# 开启网格
# plt.grid()
# 修改 x轴标度
plt.xticks(np.arange(1200, 6400, 400))
# fig = plt.figure(figsize=(10,6)) 设置图片大小
plt.show()

