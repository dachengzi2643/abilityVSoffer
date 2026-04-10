import streamlit as st
import random

# ===================== 【映射表 100% 和你原版一样】 =====================
area_map = {
    3: "SSP offer",
    2: "SP offer",
    1: "白菜offer"
}
offer_to_area = {v: k for k, v in area_map.items()}

abi_area_map = {
    "a": 3,
    "b": 2,
    "c": 1
}

role_level = {"normal": 1, "super": 2, "admin": 3}
role_list = ["normal", "super", "admin"]
abi_list = ["a", "b", "c"]


# ===================== 【核心计算函数 100% 照搬】 =====================
def get_area(role, abi):
    if role == "admin":
        return 2
    elif role == "super":
        if abi == "a":
            return 3
        elif abi == "b":
            return 2
        else:
            return 1
    elif role == "normal":
        return 1
    return 1


def is_role_legal(old, new):
    return abs(role_level[old] - role_level[new]) == 1


# ===================== 界面 =====================
st.title("abilityVSoffer")
st.markdown("## 此游戏仅供娱乐，发散思维，ai编程，其乐无穷")

# ===================== 规则表（和你 GUI 一模一样） =====================
st.subheader("权限-能力-区域规则表")
st.code("""
admin   任意    区域2    SP offer
super   a      区域3    SSP offer
super   b      区域2    SP offer
super   c      区域1    白菜offer
normal  任意    区域1    白菜offer
""")

mode = st.radio("模式切换", ["默认模式", "极难模式"], horizontal=True)
st.divider()

# ======================================
# 默认模式：随机初始 + 修改 + 计算
# ======================================
if mode == "默认模式":
    st.markdown("### 默认模式")

    # 初始化缓存
    if "init_role" not in st.session_state:
        st.session_state.init_role = ""
    if "init_abi" not in st.session_state:
        st.session_state.init_abi = ""

    # 按钮：随机初始 【完全一样】
    if st.button("随机初始"):
        r = random.choice(role_list)
        a = random.choice(abi_list)
        st.session_state.init_role = r
        st.session_state.init_abi = a

    ir = st.session_state.init_role
    ia = st.session_state.init_abi

    # 修改项
    nr = st.selectbox("修改权限", role_list)
    na = st.selectbox("修改能力", abi_list)

    # 计算
    ioff = area_map[get_area(ir, ia)] if ir else ""
    noff = area_map[get_area(nr, na)]

    # 输出
    st.markdown(f"初始：[{ir} | {ia}] → {ioff}")
    st.markdown(f"修改：[{nr} | {na}] → {noff}")

# ======================================
# 极难模式：定向随机初始 + 计算结果
# ======================================
else:
    st.markdown("### 极难模式")

    if "h_role" not in st.session_state:
        st.session_state.h_role = ""
    if "h_offer" not in st.session_state:
        st.session_state.h_offer = ""

    # 按钮：定向随机初始 【完全一样】
    if st.button("定向随机初始"):
        role = random.choice(["normal", "admin"])

        # ========== 你原版逻辑，我完全没改 ==========
        if role == "admin":
            to = "白菜offer"
        else:
            to = "SP offer"

        st.session_state.h_role = role
        st.session_state.h_offer = to

    # 显示
    st.write("当前权限：", st.session_state.h_role)
    st.write("目标Offer：", st.session_state.h_offer)

    abi = st.selectbox("修改能力", abi_list)

    # 按钮：计算结果 【完全一样】
    if st.button("计算结果"):
        hr = st.session_state.h_role
        ho = st.session_state.h_offer

        if not hr or not ho:
            st.warning("请先点击 定向随机初始")
        else:
            ab_a = abi_area_map[abi]
            of_a = offer_to_area[ho]

            st.markdown(f"当前权限：{hr}")
            st.markdown(f"当前能力：{abi}")
            st.markdown(f"对应Offer：{ho}")
            st.divider()

            # ========== 判断逻辑 100% 一样 ==========
            if ab_a > of_a:
                st.success(f"能力为{abi}，你为什么不去找更好的offer？")
            else:
                st.warning(f"能力为{abi}，你觉得你能胜任这个offer吗？")
