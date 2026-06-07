import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===================== 页面配置 =====================
st.set_page_config(page_title="牛顿环实验-线性拟合法", layout="centered")
st.title("🔬 牛顿环实验数据处理（线性拟合法）")
st.markdown("### 适配级数：11 ~ 20 级")
st.divider()

# ===================== 固定参数 =====================
lambda_light = 589.3e-9  # 钠光波长
k_list = list(range(11, 21))  # 11,12...20

# ===================== 输入读数 =====================
st.subheader("1. 输入暗环左右读数（单位：mm）")
x1_list = []
x2_list = []

col1, col2 = st.columns(2)
for i in range(10):
    k_num = k_list[i]
    with col1:
        left = st.number_input(f"第{k_num}级 左读数", key=f"l{k_num}", format="%.3f")
    with col2:
        right = st.number_input(f"第{k_num}级 右读数", key=f"r{k_num}", format="%.3f")
    x1_list.append(left)
    x2_list.append(right)

st.divider()

# ===================== 计算按钮 =====================
if st.button("🧮 开始计算 + 绘制 D²-k 图", type="primary"):
    st.subheader("2. 计算过程")

    # --------------------- 1. 计算直径 D 和 D² ---------------------
    D = np.abs(np.array(x1_list) - np.array(x2_list))
    D2 = D ** 2  # 直径平方，单位 mm²

    # 显示每一级结果
    for i in range(10):
        st.write(f"第{k_list[i]}级：D = {D[i]:.3f} mm  |  D² = {D2[i]:.4f} mm²")

    # --------------------- 2. 线性拟合（最小二乘法）---------------------
    # 构造矩阵 X = [k, 1]
    X = np.vstack([k_list, np.ones(len(k_list))]).T
    a, b = np.linalg.lstsq(X, D2, rcond=None)[0]

    # 计算曲率半径 R
    # ====================== 【唯一修改：加上 ×1e-6 单位换算】 ======================
    R = (a * 1e-6) / (4 * lambda_light)
    # ==============================================================================

    st.divider()
    st.markdown("### 🎯 拟合结果")
    st.write(f"✅ 斜率 a = {a:.4f} mm²/级")
    st.write(f"✅ 截距 b = {b:.4f} mm²")
    st.success(f"📏 凸透镜曲率半径 R = {R:.4f} 米")
    st.success(f"📏 R = {R * 100:.2f} 厘米")

    # --------------------- 3. 计算总误差（点到直线距离和）---------------------
    total_error = 0
    for i in range(10):
        y_fit = a * k_list[i] + b
        dist = abs(y_fit - D2[i]) / np.sqrt(1 + a**2)
        total_error += dist
    st.write(f"📉 所有点到直线总误差 = {total_error:.4f}")

    # --------------------- 4. 绘图 D² — k 关系曲线 ---------------------
    st.divider()
    st.subheader("3. D² — k 关系曲线图")

    # 解决中文显示
    plt.rcParams["font.family"] = ["SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 5))

    # 画实验数据点
    ax.plot(k_list, D2, "o", color="#1f77b4", markersize=8, label="实验数据点")

    # 画拟合直线
    k_fit = np.linspace(11, 20, 100)
    D2_fit = a * k_fit + b
    ax.plot(k_fit, D2_fit, "-", color="#ff4b5c", linewidth=2, label="拟合直线")

    # 图表样式
    ax.set_title("牛顿环 D² — k 关系曲线", fontsize=14, fontweight="bold")
    ax.set_xlabel("暗环级数 k", fontsize=12)
    ax.set_ylabel("直径平方 D² (mm²)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()

    st.pyplot(fig)

    st.divider()
    st.balloons()
    st.markdown("## ✅ 数据处理完成！")