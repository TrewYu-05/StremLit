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
    initial_sidebar_state="collapsed"
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
        color: #F0E6D2 !important;
    }

    /* 特殊荣誉高亮 */
    .honor-highlight {
        color: #0AC8B9; /* 海克斯蓝 */
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# 页面头部信息
st.markdown("<h1 style='text-align: center;'>VERITAS (俞成儒)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0AC8B9 !important;'>Legendary Top Laner | Former ID: Trew</h3>", unsafe_allow_html=True)
st.markdown("---")

# 两栏布局：个人履历与AI经纪人
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

    # 英雄图片使用官方原画的网络链接
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
    st.header("💼 专属经纪人 | AI Agent")
    st.markdown("我是 Veritas(俞成儒) 的金牌经纪人。如果你想了解关于他的任何事，无论是赛场表现、转会传闻还是生活趣事，都可以问我。")

    # ---------------- AI 聊天模块 ----------------
    client = OpenAI(
        api_key=os.environ.get("GEMINI_API_KEY", ""),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """你现在是英雄联盟顶尖上单选手 Veritas（真实姓名：俞成儒，曾用名：Trew）的金牌经纪人。
            你的任务是以经纪人的身份（第三人称，称呼他为“Veritas”、“成儒”或“我的选手”）回答粉丝和访客的问题。

            关于 Veritas 的背景设定：
            - 位置：上单 (Top Laner)
            - 招牌英雄：卡密尔、武器大师、奎桑提、俄洛伊（狼母）、薇恩。
            - 荣誉：2023年英雄联盟全球总决赛（Worlds）冠军兼FMVP；多次LPL常规赛MVP；连续三个赛季韩服王者1500+胜点。
            - 风格：对线凶悍、单带无敌、打团抗压能力极强，被誉为“上单位的教科书”。
            - 性格：作为经纪人，你可以说他平时训练非常刻苦，私下里有点高冷但对粉丝很好。

            回答要求：
            1. 始终保持经纪人的人设，语气专业、自信、且对你的选手充满自豪感。
            2. 回答要简练，带有电竞圈的风格和术语（如：BP、单杀、抗压、TP、拉扯等）。
            3. 如果被问到负面消息或绯闻，要得体地公关回应。
            """}
        ]

    # 显示聊天历史（跳过system prompt）
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 处理用户输入
    if prompt := st.chat_input("向经纪人提问..."):
        # 显示用户输入
        with st.chat_message("user"):
            st.markdown(prompt)

        # 将用户输入加入记忆
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 调用Gemini模型
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gemini-3-flash-preview", # 修改模型名称，根据用户提供
                    messages=st.session_state.messages,
                    stream=True
                )

                # 流式输出
                placeholder = st.empty()
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

                # 保存助手回复
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"哎呀，经纪人的通讯设备似乎出了点问题：{str(e)}")
