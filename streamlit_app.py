import streamlit as st
import pandas as pd
import numpy as np
import math

# ==============================================================================
# 1. 基础配置与参考文献/动作库
# ==============================================================================
st.set_page_config(
    page_title="Program Architect V1.1", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 这一段能让手机端在打开时，不会因为缩放问题导致文字太小
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# 动作词典
EXERCISE_GLOSSARY = {
    "Pause Squat": "暂停深蹲。在最低点（坑底）完全静止 1-2 秒。目的：消除牵张反射，强化底部启动力量。",
    "Leg Press": "腿举。固定器械。目的：在不增加下背部压力的情况下，极大地增加股四头肌的代谢压力。",
    "RDL (Romanian Deadlift)": "罗马尼亚硬拉。膝盖微屈锁定，靠屈髋下放。目的：针对性强化腘绳肌（后链）和臀部。",
    "Leg Curl": "腿弯举。目的：唯一能完全孤立腘绳肌膝屈功能的动作，预防膝盖受伤。",
    "Back Extension": "背屈伸（山羊挺身）。目的：强化竖脊肌的耐力，增加下背部抗疲劳能力。",
    "DB Overhead Press": "哑铃肩推。目的：增加肩部维度，哑铃提供更大的活动范围和稳定性挑战。",
    "Chest Support Row": "胸部支撑划船。目的：完全孤立背部肌群，避免借力，保护下背部。",
    "Tricep Pushdown": "三头肌下压。目的：增加上臂围度，强化肘关节锁定能力。",
    "Close-Grip Bench": "窄距卧推。握距比比赛握距窄 2-3 指。目的：大幅增加三头肌参与，解决“推不开”的问题。",
    "Spoto Press": "凌空暂停卧推。在胸口上方 2-3cm 处暂停。目的：提高对杠铃的控制力，强化中段力量。",
    "Pull-ups": "引体向上。目的：背阔肌垂直拉力，构建倒三角体型，通过肩胛稳定性辅助卧推。",
    "Dips": "双杠臂屈伸。目的：极佳的上肢复合推类动作，同时刺激胸大肌下沿和三头肌。",
    "Face Pulls": "面拉。目的：强化肩袖肌群和后束，对抗卧推带来的圆肩风险，保持肩部健康。"
}

# 参考文献库
REFERENCES = {
    "Specificity": {
        "title": "Specificity (特异性)",
        "source": "Scientific Principles of Strength Training, Ch.3",
        "desc": "训练必须针对特定目标（力量举）进行优化。越接近比赛，专项性越高。"
    },
    "Overload": {
        "title": "Overload (超负荷)",
        "source": "Scientific Principles of Strength Training, Ch.4",
        "desc": "必须提供超出习惯的刺激才能引发适应。本程序通过非线性波浪实现超负荷。"
    },
    "Fatigue": {
        "title": "Fatigue Management (疲劳管理)",
        "source": "Scientific Principles, Ch.5 & Juggernaut Method",
        "desc": "疲劳的累积会掩盖体能。必须通过减载（Deload Week）消除系统性疲劳。"
    },
    "SRA": {
        "title": "SRA Curve (刺激-恢复-适应)",
        "source": "Scientific Principles, Ch.6",
        "desc": "不同强度的训练需要不同的恢复时间。减载周决定了适应曲线的完整性。"
    },
    "Phase": {
        "title": "Phase Potentiation (相位增强)",
        "source": "Scientific Principles, Ch.8",
        "desc": "积累期的肌肥大为力量期打基础，力量期为顶峰期打基础。"
    },
    "Individual": {
        "title": "Individual Differences (个体差异)",
        "source": "Scientific Principles, Ch.9",
        "desc": "由于杠杆比例不同，辅助项（Accessory）的选择应基于个人弱点。"
    }
}

def round_to_plates(weight):
    return math.floor(weight / 2.5 + 0.5) * 2.5

# ==============================================================================
# 2. 视觉样式 CSS (修正手机端侧边栏按钮消失问题)
# ==============================================================================
st.markdown("""
<style>
    /* 1. 基础布局 */
    .stApp { background-color: #F8F9FA; color: #2D3748; }
    
    /* 修正：不再彻底隐藏 header，而是只隐藏装饰物，保留侧边栏开关 */
    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important; /* 背景透明 */
        color: #2D3748 !important;
    }
    /* 隐藏右侧的部署按钮、菜单按钮，只留左侧的侧边栏控制 */
    button[data-testid="stHeaderDeployButton"], 
    button[data-testid="stHeaderMenuButton"] {
        display: none !important;
    }
    
    .block-container { padding-top: 2.5rem !important; }

    /* 2. 侧边栏样式 */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }

    /* 3. 滑块样式 (保持蓝色，消除红色) */
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background-color: #e5e7eb !important;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div {
        background-color: #3B82F6 !important;
    }
    div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #3B82F6 !important;
    }

    /* 4. 训练卡片美化 */
    .train-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .card-header { font-size: 0.85em; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
    .main-lift { font-size: 1.4em; font-weight: 800; color: #111827; }
    .load-text { font-family: 'Roboto Mono', monospace; color: #2563EB; font-weight: 700; font-size: 1.2em; }
    .acc-list { margin-top: 15px; padding-top: 15px; border-top: 1px dashed #E5E7EB; font-size: 0.9em; list-style-type: none; padding-left: 0; }
    .acc-list li { margin-bottom: 6px; padding-left: 12px; border-left: 3px solid #E5E7EB; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. 核心引擎类 (保持非线性逻辑)
# ==============================================================================
class ProgramEngine:
    def __init__(self, s, b, d, target_s, target_b, target_d, weeks):
        self.current = {"S": s, "B": b, "D": d}
        self.target = {"S": target_s, "B": target_b, "D": target_d}
        self.weeks = weeks
        self.total_gain_pct = ((target_s+target_b+target_d) - (s+b+d)) / (s+b+d)

    def evaluate_goal(self):
        monthly_rate = self.total_gain_pct / (self.weeks / 4)
        if monthly_rate <= 0.015: return "稳健 (Conservative)", "green"
        elif monthly_rate <= 0.035: return "适中 (Realistic)", "orange"
        else: return "激进 (Aggressive)", "red"

    def get_phase_info(self, week):
        ratio = week / self.weeks
        is_deload = (week % 4 == 0) and (week != self.weeks)
        if is_deload: return {"name": "Deload (减载周)", "color": "#10B981", "desc": "消散疲劳，恢复神经系统。", "acc_strategy": "Recovery"}
        elif ratio <= 0.4: return {"name": "Accumulation (积累期)", "color": "#3B82F6", "desc": "高容量、中低强度。建立肌肉储备。", "acc_strategy": "Hypertrophy"}
        elif ratio <= 0.75: return {"name": "Transmutation (转化期)", "color": "#F59E0B", "desc": "强度提升，向专项力量转化。", "acc_strategy": "Strength"}
        else: return {"name": "Realization (实现期)", "color": "#EF4444", "desc": "低容量、极限强度。展现最高水平。", "acc_strategy": "Maintenance"}

    def calculate_weekly_load(self, week, lift_type):
        theoretical_max = self.current[lift_type] + (self.target[lift_type] - self.current[lift_type]) * (week / self.weeks)
        phase = self.get_phase_info(week)
        wave_pos = 4 if "Deload" in phase['name'] else week % 4
        if wave_pos == 0: wave_pos = 3 
        
        if "Accumulation" in phase['name']:
            reps, base_pct, sets, rpe = (8 if lift_type != "D" else 5), 0.65, (4 + (1 if wave_pos >=2 else 0)), (6 + wave_pos)
        elif "Transmutation" in phase['name']:
            reps, base_pct, sets, rpe = (5 if lift_type != "D" else 3), 0.78, 4, (7 + (wave_pos * 0.5))
        elif "Realization" in phase['name']:
            reps, base_pct, sets, rpe = 2, 0.88, 3, (7 + wave_pos)
        else: # Deload
            reps, base_pct, sets, rpe = 5, 0.50, 2, 5

        intensity_mod = (wave_pos - 1) * 0.025
        if "Deload" in phase['name']: intensity_mod = 0
        return round_to_plates(theoretical_max * (base_pct + intensity_mod)), sets, reps, rpe

    def calculate_accessories(self, week):
        phase = self.get_phase_info(week)
        strategy = phase['acc_strategy']
        wave_pos = 4 if "Deload" in phase['name'] else week % 4
        if wave_pos == 0: wave_pos = 3
        
        if "Recovery" in strategy: return "2 Sets", "10-12 Reps", "RPE 6"
        elif "Hypertrophy" in strategy:
            sets = 3 + (1 if wave_pos >= 2 else 0)
            return f"{sets} Sets", "10-15 Reps", f"RPE {7 + (wave_pos - 1)}"
        elif "Strength" in strategy:
            return "3 Sets", "8-10 Reps", f"RPE {7.5 + (wave_pos * 0.5)}"
        else: return "2 Sets", "6-8 Reps", "RPE 7"

# ==============================================================================
# 4. 侧边栏与作者标识
# ==============================================================================
st.sidebar.markdown("### 👤 作者：石恩泽")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 档案 (Profile)")
c_s = st.sidebar.number_input("深蹲 Current", 200, step=5)
c_b = st.sidebar.number_input("卧推 Current", 140, step=5)
c_d = st.sidebar.number_input("硬拉 Current", 220, step=5)

st.sidebar.markdown("### 🎯 目标 (Goal)")
weeks_total = st.sidebar.slider("周期长度 (Weeks)", 10, 24, 16)
t_s = st.sidebar.number_input("目标 深蹲", int(c_s*1.05), step=2)
t_b = st.sidebar.number_input("目标 卧推", int(c_b*1.05), step=2)
t_d = st.sidebar.number_input("目标 硬拉", int(c_d*1.05), step=2)

engine = ProgramEngine(c_s, c_b, c_d, t_s, t_b, t_d, weeks_total)
eval_status, eval_color = engine.evaluate_goal()

# ==============================================================================
# 5. 主界面渲染
# ==============================================================================
st.title("Program Architect V1.1")
st.caption("基于三本核心著作构建的非线性力量举引擎 | 作者：石恩泽")

col1, col2, col3 = st.columns(3)
col1.metric("Training Time", f"{weeks_total} 周")
col2.metric("Target Total", f"{t_s+t_b+t_d} kg")
with col3:
    st.markdown("**可行性评估**")
    st.markdown(f"<span style='color:{eval_color}; font-weight:bold; font-size:1.2em'>{eval_status}</span>", unsafe_allow_html=True)

st.divider()

# 周期导航
st.subheader("📍 周期导航 (Week Selector)")
selected_week = st.slider("Timeline", 1, weeks_total, 1, label_visibility="collapsed")

# 获取本周数据
phase = engine.get_phase_info(selected_week)
s_w, s_s, s_r, s_rpe = engine.calculate_weekly_load(selected_week, "S")
b_w, b_s, b_r, b_rpe = engine.calculate_weekly_load(selected_week, "B")
d_w, d_s, d_r, d_rpe = engine.calculate_weekly_load(selected_week, "D")
acc_s, acc_r, acc_rp = engine.calculate_accessories(selected_week)

# 阶段解释卡片
st.markdown(f"""
<div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 8px solid {phase['color']}; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
    <h3 style="margin:0; color: {phase['color']};">{phase['name']} - Week {selected_week}</h3>
    <p style="margin-top: 8px; color: #4B5563;">{phase['desc']}</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# 训练卡片渲染函数
def render_card(title, color, lift, weight, sets, reps, rpe, accessories):
    acc_html = "".join([f"<li>{acc}</li>" for acc in accessories])
    return f"""
    <div class="train-card" style="border-top: 4px solid {color};">
        <div class="card-header" style="color: {color};">{title}</div>
        <div class="main-lift">{lift}</div>
        <div style="margin: 12px 0;"><span class="load-text">{weight} kg</span><span style="color:#6B7280; margin-left:8px;">{sets} x {reps}</span></div>
        <div style="margin-bottom: 20px;"><span style="background-color:#E5E7EB; padding:4px 8px; border-radius:4px; font-size:0.9em; font-weight:600;">RPE {rpe}</span></div>
        <div style="background-color:#F9FAFB; padding:12px; border-radius:8px;">
            <ul class="acc-list" style="margin:0; padding:0;">{acc_html}</ul>
        </div>
    </div>
    """

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(render_card("Day 1: Squat", phase['color'], "Competition Squat", s_w, s_s, s_r, s_rpe, [f"Pause Squat: {acc_s} x {acc_r}", f"Leg Press: {acc_s} x 12", "Core: 3 Sets"]), unsafe_allow_html=True)
with c2:
    st.markdown(render_card("Day 2: Bench", phase['color'], "Competition Bench", b_w, b_s, b_r, b_rpe, [f"DB OH Press: {acc_s} x 10", f"Chest Support Row: {acc_s} x {acc_r}", "Tricep Pushdown: 3 Sets"]), unsafe_allow_html=True)
with c3:
    st.markdown(render_card("Day 3: Deadlift", phase['color'], "Competition Deadlift", d_w, max(2, d_s-1), d_r, d_rpe, [f"RDL (罗马尼亚): {acc_s} x 8", f"Leg Curl: {acc_s} x 15", "Back Extension: 3 Sets"]), unsafe_allow_html=True)
with c4:
    var_w = round_to_plates(b_w * 0.9)
    st.markdown(render_card("Day 4: Bench Variation", phase['color'], "Close-Grip / Spoto", var_w, b_s, b_r, max(6, b_rpe-0.5), [f"Pull-ups: {acc_s} x AMRAP", f"Dips: {acc_s} x 10", "Face Pulls: 3 x 20"]), unsafe_allow_html=True)

# ==============================================================================
# 6. 底部信息：参考文献与动作说明
# ==============================================================================
st.divider()
f1, f2 = st.columns(2)

with f1:
    st.subheader("📚 参考文献 (References)")
    with st.expander("点击查看核心训练原理", expanded=True):
        for key, val in REFERENCES.items():
            st.markdown(f"**{val['title']}**")
            st.caption(f"{val['desc']} —— *{val['source']}*")
            st.write("")

with f2:
    st.subheader("🏋️ 动作词典 (Exercise Glossary)")
    with st.expander("点击查看辅助动作解析", expanded=True):
        for key, val in EXERCISE_GLOSSARY.items():
            st.write(f"**{key}**: {val}")
            st.write("---")

st.caption("Program Architect V1.1 | 作者：石恩泽 | 状态：正式版本发布")