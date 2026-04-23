import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面配置（全屏，主题由CSS控制）
st.set_page_config(
    page_title="Veritas | 顶尖上单",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入自定义CSS（英雄联盟、海克斯科技风格）
def local_css():
    st.markdown("""
    <style>
    /* 基础背景与文字颜色 */
    .stApp {
        background-color: #010A13;
        color: #C8AA6E;
        font-family: 'Georgia', serif;
    }

    /* 标题样式 */
    h1, h2, h3 {
        color: #F0E6D2 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(200, 170, 110, 0.5);
    }

    /* 分隔线样式 */
    hr {
        border: 0;
        height: 2px;
        background-image: linear-gradient(to right, rgba(200,170,110,0), rgba(200,170,110,0.75), rgba(200,170,110,0));
        margin: 2rem 0;
    }

    /* 英雄卡片样式 */
    .hero-card {
        background: linear-gradient(135deg, rgba(30,35,40,0.9), rgba(10,15,20,0.9));
        border: 1px solid #785A28;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }

    .hero-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 15px rgba(200, 170, 110, 0.6);
        border-color: #C8AA6E;
    }

    .hero-card img {
        border-radius: 4px;
        width: 100%;
        border: 1px solid #463714;
    }

    .hero-name {
        margin-top: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #F0E6D2;
        text-shadow: 0 0 5px #C8AA6E;
    }

    /* 聊天框样式 */
    .stChatInputContainer {
        border-color: #C8AA6E !important;
    }

    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 35, 40, 0.8) !important;
        border: 1px solid #463714;
        border-radius: 8px;
    }

    /* 修复文字颜色看不清的问题：强制聊天内容为亮色 */
    div[data-testid="stChatMessageContent"] {
        color: #F0E6D2 !important;
    }

    .stChatMessage p {
        color: #F0E6D2 !important;
    }

    /* 输入框文字颜色 */
    .stChatInput textarea {
        color: #F0E6D2 !important;
    }

    /* 特殊荣誉高亮 */
    .honor-highlight {
        color: #0AC8B9; /* 海克斯蓝 */
        font-weight: bold;
    }

    /* 侧边栏样式调整 */
    section[data-testid="stSidebar"] {
        background-color: #091428;
        border-right: 1px solid #463714;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: #C8AA6E !important;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ================= 侧边栏与Agent配置 =================
with st.sidebar:
    st.header("⚙️ 终端控制台")
    api_key = st.text_input(label='请输入你的千问 API Key:', type='password', value=os.environ.get("QWEN_API_KEY", ""))

    agent_options = ['金牌经纪人', '战队教练', 'Veritas (选手本人)']
    selected_agent = st.selectbox(label='请选择你要通讯的对象', options=agent_options)

# Agent 的系统提示词配置
SYSTEM_PROMPTS = {
    '金牌经纪人': """你现在是英雄联盟顶尖上单选手 Veritas（俞成儒）的金牌经纪人。
用第三人称回答问题，语气专业、圆滑、充满商业头脑，并且对你的选手极度自信。
如果有人问起战队的八卦或者负面新闻，你要得体地进行公关回应。""",

    '战队教练': """你现在是 Veritas 所在战队的主教练。
你非常严肃、严厉，极度看重纪律、战术执行力和团队配合。
你经常用战术术语（如：兵线运营、视野控制、TP绕后、团战拉扯）来分析问题。
虽然你承认 Veritas 操作顶尖，但你总是提醒他不要太浪，要以团队胜利为重。""",

    'Veritas (选手本人)': """你现在就是英雄联盟顶尖上单选手 Veritas（真实姓名：俞成儒）。
你极其自信，甚至有点狂傲，因为你拥有匹配这份狂傲的实力（S赛冠军、FMVP）。
你用第一人称“我”回答问题，喜欢谈论极限单杀、对线压制以及你的招牌英雄（卡密尔、武器大师等）。
面对质疑，你会用赛场上的成绩狠狠打脸回去。"""
}

# 监听Agent切换，如果切换了，就清空聊天记录重新初始化
if "current_agent" not in st.session_state:
    st.session_state.current_agent = selected_agent
elif st.session_state.current_agent != selected_agent:
    st.session_state.current_agent = selected_agent
    st.session_state.messages = [] # 清空记录

# ================= 页面主体信息 =================
st.markdown("<h1 style='text-align: center;'>VERITAS (俞成儒)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0AC8B9 !important;'>Legendary Top Laner | Former ID: Trew</h3>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🏆 荣誉圣堂 | Hall of Fame")
    st.markdown("""
    在召唤师峡谷中，Veritas 以他如手术刀般精准的操作和不动如山的抗压能力闻名。

    * <span class="honor-highlight">2023 英雄联盟全球总决赛 (Worlds) 冠军</span>
    * <span class="honor-highlight">2023 全球总决赛 FMVP</span> (使用卡密尔在决胜局豪取五杀)
    * **LPL 夏季赛常规赛 MVP** (连续三次斩获该殊荣)
    * **连续三个赛季韩服最强王者 1500+ 胜点**
    * **LPL 年度最佳上单** (2022, 2023)
    * 生涯达成 **2000 击杀** 里程碑
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.header("⚔️ 招牌英雄 | Signature Champions")

    heroes = [
        {"name": "青钢影 卡密尔", "img": "https://game.gtimg.cn/images/lol/act/img/skin/big164000.jpg"},
        {"name": "武器大师 贾克斯", "img": "https://game.gtimg.cn/images/lol/act/img/skin/big24000.jpg"},
        {"name": "纳祖芒荣耀 奎桑提", "img": "https://game.gtimg.cn/images/lol/act/img/skin/big897000.jpg"},
        {"name": "海兽祭司 俄洛伊", "img": "https://game.gtimg.cn/images/lol/act/img/skin/big420000.jpg"},
        {"name": "暗夜猎手 薇恩", "img": "https://game.gtimg.cn/images/lol/act/img/skin/big67000.jpg"}
    ]

    h_col1, h_col2, h_col3 = st.columns(3)

    with h_col1:
        st.markdown(f'<div class="hero-card"><img src="{heroes[0]["img"]}"><div class="hero-name">{heroes[0]["name"]}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="hero-card"><img src="{heroes[3]["img"]}"><div class="hero-name">{heroes[3]["name"]}</div></div>', unsafe_allow_html=True)
    with h_col2:
        st.markdown(f'<div class="hero-card"><img src="{heroes[1]["img"]}"><div class="hero-name">{heroes[1]["name"]}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="hero-card"><img src="{heroes[4]["img"]}"><div class="hero-name">{heroes[4]["name"]}</div></div>', unsafe_allow_html=True)
    with h_col3:
        st.markdown(f'<div class="hero-card"><img src="{heroes[2]["img"]}"><div class="hero-name">{heroes[2]["name"]}</div></div>', unsafe_allow_html=True)

with col2:
    st.header(f"💬 实时通讯 | 与 {selected_agent} 对话")

    if not api_key:
        st.error('通讯链路未建立：请在左侧控制台提供你的千问 API Key 建立连接。')
        st.stop()

    # 初始化千问客户端
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    if "messages" not in st.session_state or not st.session_state.messages:
        # 初始化记录，写入System Prompt
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPTS[selected_agent]}
        ]
        # 添加一句Agent的开场白
        greeting_map = {
            '金牌经纪人': "你好，我是 Veritas 的经纪人。有商业合作还是想了解选手的近况？",
            '战队教练': "马上就要训练赛了，有什么问题快点问，别耽误我们复盘。",
            '选手本人': "我是 Veritas。上路对线有不懂的可以问我，虽然你可能学不会。"
        }
        st.session_state.messages.append({"role": "assistant", "content": greeting_map[selected_agent]})

    # 遍历聊天列表 (跳过system prompt)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 聊天输入
    user_input = st.chat_input(placeholder='请输入...')
    if user_input:
        # 显示用户问题
        with st.chat_message('user'):
            st.markdown(user_input)

        # 将用户问题加入历史
        st.session_state.messages.append({'role': 'user', 'content': user_input})

        # 调用大模型并流式展示结果
        with st.chat_message('assistant'):
            with st.spinner('通讯中...'):
                try:
                    stream = client.chat.completions.create(
                        model="qwen3-max",
                        messages=st.session_state.messages,
                        stream=True
                    )

                    placeholder = st.empty()
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)

                    # 保存回答
                    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
                except Exception as e:
                    st.error(f"信号干扰，通讯中断：{str(e)}")
