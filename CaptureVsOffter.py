import random
import tkinter as tk
from tkinter import ttk, messagebox

# ===================== 规则 =====================
# Offer区域：越大越好
area_map = {
    3: "SSP offer",
    2: "SP offer",
    1: "白菜offer"
}
offer_to_area = {v: k for k, v in area_map.items()}

# 能力区域：越大越好
abi_area_map = {
    "a": 3,
    "b": 2,
    "c": 1
}

role_level = {"normal": 1, "super": 2, "admin": 3}
role_list = ["normal", "super", "admin"]
abi_list = ["a", "b", "c"]

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

# ===================== 主界面 =====================
class AbilityVSOfferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("abilityVSoffer")
        self.geometry("920x680")
        self.resizable(False, False)

        self.mode = tk.StringVar(value="normal")

        # 默认模式
        self.n_init_role = tk.StringVar()
        self.n_init_abi = tk.StringVar()
        self.n_init_offer = tk.StringVar()
        self.n_new_role = tk.StringVar()
        self.n_new_abi = tk.StringVar()
        self.n_new_offer = tk.StringVar()
        self.n_covered = set()

        # 极难模式
        self.h_role = tk.StringVar()
        self.h_new_abi = tk.StringVar()
        self.h_target_offer = tk.StringVar()

        # ================== 顶部 ==================
        top = tk.Frame(self, pady=10)
        top.pack(fill=tk.X)
        tk.Label(top, text="权限", font=("SimHei", 13, "bold")).grid(row=0, column=0, padx=40)
        tk.Label(top, text="能力", font=("SimHei", 13, "bold")).grid(row=0, column=1, padx=40)
        tk.Label(top, text="Offer", font=("SimHei", 13, "bold")).grid(row=0, column=2, padx=40)

        # ================== 提示文字（在规则表上方） ==================
        tip_label = tk.Label(self,
                           text="此游戏仅供娱乐，发散思维，ai编程，其乐无穷",
                           font=("SimHei", 12, "bold"),
                           fg="#d63031")
        tip_label.pack(pady=5)

        # ================== 规则表 ==================
        rule_frm = tk.LabelFrame(self, text="权限-能力-区域规则表", font=("SimHei", 11), padx=10, pady=6)
        rule_frm.pack(fill=tk.X, padx=20)
        cols = ("权限", "能力", "对应区域", "Offer")
        tree = ttk.Treeview(rule_frm, columns=cols, show="headings", height=7)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160, anchor=tk.CENTER)
        rules = [
            ("admin", "任意", "区域2", "SP offer"),
            ("super", "a", "区域3", "SSP offer"),
            ("super", "b", "区域2", "SP offer"),
            ("super", "c", "区域1", "白菜offer"),
            ("normal", "任意", "区域1", "白菜offer"),
        ]
        for r in rules:
            tree.insert("", tk.END, values=r)
        tree.pack()

        # ================== 模式切换 ==================
        mode_frm = tk.Frame(self, pady=5)
        mode_frm.pack(fill=tk.X)
        tk.Radiobutton(mode_frm, text="默认模式", variable=self.mode, value="normal",
                       command=self.switch_panel, font=("", 11)).pack(side=tk.LEFT, padx=30)
        tk.Radiobutton(mode_frm, text="极难模式", variable=self.mode, value="hard",
                       command=self.switch_panel, font=("", 11)).pack(side=tk.LEFT, padx=30)

        # ================== 容器 ==================
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # ---------- 默认模式面板 ----------
        self.normal_panel = tk.Frame(self.container)
        self.build_normal_panel()

        # ---------- 极难模式面板 ----------
        self.hard_panel = tk.Frame(self.container)
        self.build_hard_panel()

        self.switch_panel()

    # ================== 默认模式 ==================
    def build_normal_panel(self):
        p = self.normal_panel
        cmp_frm = tk.Frame(p, pady=12)
        cmp_frm.pack(fill=tk.X)

        left = tk.LabelFrame(cmp_frm, text="初始状态", font=("SimHei", 11))
        left.grid(row=0, column=0, padx=20, sticky=tk.NSEW)
        tk.Label(left, text="权限：").grid(row=0, column=0, padx=6, pady=8)
        tk.Label(left, textvariable=self.n_init_role, width=10).grid(row=0, column=1)
        tk.Label(left, text="能力：").grid(row=1, column=0, padx=6, pady=8)
        tk.Label(left, textvariable=self.n_init_abi, width=10).grid(row=1, column=1)
        tk.Label(left, text="Offer：").grid(row=2, column=0, padx=6, pady=8)
        tk.Label(left, textvariable=self.n_init_offer, width=20, fg="blue").grid(row=2, column=1)

        tk.Label(cmp_frm, text=" ➔ ", font=("", 18)).grid(row=0, column=1, padx=20)

        right = tk.LabelFrame(cmp_frm, text="修改后", font=("SimHei", 11))
        right.grid(row=0, column=2, padx=20, sticky=tk.NSEW)
        tk.Label(right, text="权限：").grid(row=0, column=0, padx=6, pady=8)
        ttk.Combobox(right, textvariable=self.n_new_role, values=role_list, state="readonly", width=10).grid(row=0, column=1)
        tk.Label(right, text="能力：").grid(row=1, column=0, padx=6, pady=8)
        ttk.Combobox(right, textvariable=self.n_new_abi, values=abi_list, state="readonly", width=10).grid(row=1, column=1)
        tk.Label(right, text="Offer：").grid(row=2, column=0, padx=6, pady=8)
        tk.Label(right, textvariable=self.n_new_offer, width=20, fg="red").grid(row=2, column=1)

        cmp_frm.grid_columnconfigure(0, weight=1)
        cmp_frm.grid_columnconfigure(2, weight=1)

        btn_frm = tk.Frame(p, pady=10)
        btn_frm.pack()
        tk.Button(btn_frm, text="随机初始", command=self.normal_random, width=18, bg="#eee").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frm, text="计算结果", command=self.normal_calc, width=18, bg="#cce5ff").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frm, text="清空", command=self.normal_clear, width=18, bg="#ffe5e5").pack(side=tk.LEFT, padx=12)

        res_frm = tk.LabelFrame(p, text="结果", font=("SimHei", 11), padx=10, pady=6)
        res_frm.pack(fill=tk.BOTH, expand=True)
        self.normal_res = tk.Text(res_frm, height=7, font=("SimHei", 10))
        self.normal_res.pack(fill=tk.BOTH, expand=True)

    # ================== 极难模式 ==================
    def build_hard_panel(self):
        p = self.hard_panel

        main_frm = tk.Frame(p, pady=15)
        main_frm.pack(fill=tk.X)

        role_frm = tk.LabelFrame(main_frm, text="当前权限", font=("SimHei", 11))
        role_frm.pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True)
        tk.Label(role_frm, textvariable=self.h_role, font=("",12), width=10).pack(pady=12)

        abi_frm = tk.LabelFrame(main_frm, text="修改能力", font=("SimHei", 11))
        abi_frm.pack(side=tk.RIGHT, padx=15, fill=tk.X, expand=True)
        ttk.Combobox(abi_frm, textvariable=self.h_new_abi, values=abi_list, state="readonly", width=12).pack(pady=12)

        offer_frm = tk.LabelFrame(p, text="目标Offer", font=("SimHei", 11))
        offer_frm.pack(padx=20, pady=10, fill=tk.X)
        tk.Label(offer_frm, textvariable=self.h_target_offer, font=("",12), fg="red").pack(pady=10)

        btn_frm = tk.Frame(p, pady=10)
        btn_frm.pack()
        tk.Button(btn_frm, text="定向随机初始", command=self.hard_random, width=18, bg="#eee").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frm, text="计算结果", command=self.hard_calc, width=18, bg="#cce5ff").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frm, text="清空", command=self.hard_clear, width=18, bg="#ffe5e5").pack(side=tk.LEFT, padx=12)

        res_frm = tk.LabelFrame(p, text="结果", font=("SimHei", 11), padx=10, pady=6)
        res_frm.pack(fill=tk.BOTH, expand=True)
        self.hard_res = tk.Text(res_frm, height=7, font=("SimHei", 10))
        self.hard_res.pack(fill=tk.BOTH, expand=True)

    # ================== 切换 ==================
    def switch_panel(self):
        for w in self.container.winfo_children():
            w.pack_forget()
        if self.mode.get() == "normal":
            self.normal_panel.pack(fill=tk.BOTH, expand=True)
        else:
            self.hard_panel.pack(fill=tk.BOTH, expand=True)

    # ================== 默认模式函数 ==================
    def normal_random(self):
        r = random.choice(role_list)
        a = random.choice(abi_list)
        self.n_init_role.set(r)
        self.n_init_abi.set(a)
        ar = get_area(r, a)
        self.n_init_offer.set(area_map[ar])
        self.n_covered.add(ar)
        self.n_new_role.set("")
        self.n_new_abi.set("")
        self.n_new_offer.set("")
        self.normal_res.delete(1.0, tk.END)

    def normal_clear(self):
        self.n_init_role.set("")
        self.n_init_abi.set("")
        self.n_init_offer.set("")
        self.n_new_role.set("")
        self.n_new_abi.set("")
        self.n_new_offer.set("")
        self.n_covered.clear()
        self.normal_res.delete(1.0, tk.END)

    def normal_calc(self):
        t = self.normal_res
        t.delete(1.0, tk.END)
        ir = self.n_init_role.get()
        ia = self.n_init_abi.get()
        nr = self.n_new_role.get()
        na = self.n_new_abi.get()
        if not all([ir, ia, nr, na]):
            messagebox.showwarning("提示", "请先生成初始并填写修改项")
            return
        if not is_role_legal(ir, nr):
            messagebox.showerror("错误", "权限只能跳一级！")
            return

        iarea = get_area(ir, ia)
        narea = get_area(nr, na)
        iof = area_map[iarea]
        nof = area_map[narea]
        self.n_new_offer.set(nof)
        self.n_covered.add(iarea)
        self.n_covered.add(narea)

        covered = "、".join(area_map[i] for i in sorted(self.n_covered))
        uncov = [area_map[i] for i in [1,2,3] if i not in self.n_covered]
        uncov_str = "、".join(uncov) if uncov else "全部解锁"

        t.insert(tk.END, f"初始：[{ir} | {ia}] → {iof}\n")
        t.insert(tk.END, f"修改：[{nr} | {na}] → {nof}\n\n")
        t.insert(tk.END, f"已获取：{covered}\n")
        t.insert(tk.END, f"未解锁：{uncov_str}\n")

    # ================== 极难模式函数 ==================
    def hard_random(self):
        role = random.choice(["normal", "admin"])
        self.h_role.set(role)

        if role == "admin":
            target_offer = "白菜offer"
        else:
            target_offer = "SP offer"
        self.h_target_offer.set(target_offer)

        self.h_new_abi.set("")
        self.hard_res.delete(1.0, tk.END)

    def hard_clear(self):
        self.h_role.set("")
        self.h_new_abi.set("")
        self.h_target_offer.set("")
        self.hard_res.delete(1.0, tk.END)

    def hard_calc(self):
        t = self.hard_res
        t.delete(1.0, tk.END)
        role = self.h_role.get()
        abi = self.h_new_abi.get()
        offer_str = self.h_target_offer.get()

        if not role or not abi or not offer_str:
            messagebox.showwarning("提示", "请先生成初始并选择能力")
            return

        # 核心：已按你要求反转
        abi_area = abi_area_map[abi]
        offer_area = offer_to_area[offer_str]

        t.insert(tk.END, f"当前权限：{role}\n")
        t.insert(tk.END, f"当前能力：{abi}\n")
        #t.insert(tk.END, f"对应Offer：{offer_str}\n\n")
        # 正确：当前权限 + 当前能力 → 计算出真实Offer
        real_offer = area_map[get_area(role, abi)]
        t.insert(tk.END, f"对应Offer：{real_offer}\n\n")

        # 正确判断逻辑
        if abi_area > offer_area:
            t.insert(tk.END, f"能力为{abi}，你为什么不去找更好的offer？\n")
        else:
            t.insert(tk.END, f"能力为{abi}，你觉得你能胜任这个offer吗？\n")

if __name__ == "__main__":
    app = AbilityVSOfferApp()
    app.mainloop()
