import streamlit as st
import numpy as np

# 页面基础配置
st.set_page_config(page_title="牛顿环逐差法计算(11~20级)", layout="centered")
st.title("🔬 牛顿环实验数据处理（逐差法）")
st.markdown("### 适用范围：11 ~ 20 级暗环 | 级数差 Δk = 5")
st.divider()

# ========== 固定实验参数 ==========
lambda_light = 589.3e-9   # 钠光波长
k_list = list(range(11, 21))  # 11~20级，共10级

# ========== 数据输入 ==========
st.subheader("1. 输入暗环左右读数（mm）")
x1_list = []
x2_list = []

col_left, col_right = st.columns(2)
for idx in range(10):
    ring_num = k_list[idx]
    with col_left:
        left_val = st.number_input(f"第{ring_num}级 左读数", key=f"l_{ring_num}", format="%.3f")
    with col_right:
        right_val = st.number_input(f"第{ring_num}级 右读数", key=f"r_{ring_num}", format="%.3f")
    x1_list.append(left_val)
    x2_list.append(right_val)

st.divider()

# ========== 计算主逻辑 ==========
if st.button("🧮 开始计算", type="primary"):
    st.subheader("2. 计算过程")

    # 1. 直径 D = |左 - 右|
    D = np.abs(np.array(x1_list) - np.array(x2_list))
    D_square = D ** 2

    st.markdown("#### 🔹 各级直径 & 直径平方")
    for i in range(10):
        st.write(f"第{k_list[i]}级：D = {D[i]:.3f} mm  |  D² = {D_square[i]:.6f} mm²")

    # 2. 逐差法（Δk=5）
    Dsum = 0
    # 11~15 与 16~20 逐差（共5组，标准逐差法）
    for i in range(5):
        Dsum += D_square[i+5] - D_square[i]

    Dk_avg = Dsum / 5
    # ====================== 关键修改 ======================
    # 原来 12 → 现在改为 20（因为 4×Δk = 4×5 = 20）
    R = Dk_avg / (20 * lambda_light * 1e6)
    # ======================================================

    st.divider()
    st.markdown("#### 🔹 逐差法结果（Δk=5）")
    st.write(f"逐差总和 Dsum = {Dsum:.6f} mm²")
    st.write(f"逐差平均 Dk = {Dk_avg:.6f} mm²")
    st.success(f"凸透镜曲率半径 R = {R:.4f} 米")
    st.success(f"R = {R * 100:.2f} 厘米")

    # 3. 拟合 + 误差
    a = 4 * lambda_light * R * 1e6
    b = 11.4666
    total_error = 0
    for i in range(10):
        k = k_list[i]
        y_fit = a * k + b
        distance = abs(y_fit - D_square[i]) / np.sqrt(1 + a ** 2)
        total_error += distance

    st.divider()
    st.markdown("#### 🔹 线性拟合误差")
    st.write(f"斜率 a = {a:.6f}")
    st.write(f"截距 b = {b:.4f}")
    st.write(f"总误差（距离和）= {total_error:.6f}")

    st.divider()
    st.balloons()
    st.markdown("## ✅ 计算完成！")