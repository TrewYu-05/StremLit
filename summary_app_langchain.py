import requests
from bs4 import BeautifulSoup
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

user_prompt_template = '''
你是一个根据网页标题和内容生成摘要的优秀助手，请你根据我提供的标题和内容生成markdown格式的网页摘要。
注意：摘要中不要包含```markdown和```标签，将内容控制在1000个字符以内，尽可能用列表的形式呈现内容。
### 输出格式 ###
```markdown
## <标题>
### <第一部分>
- <内容1>
- <内容2>
- <内容3>
### <第二部分>
- <内容1>
- <内容2>
- <内容3>
### ...
### 总结
<总结内容>
```
### 网页标题和内容如下所示 ###
网页标题：{title}
主体内容：{body}
'''

prompt = PromptTemplate(
    input_variables=["title", "body"],
    template=user_prompt_template
)

def fetch_page(url):
    try:
        resp = requests.get(
            url=url,
            headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3'
            },
            timeout=10
        )
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for elem in soup.body(['script', 'link', 'nav', 'header', 'footer', 'form', 'input', 'button', 'img', 'audio', 'video', 'area', 'canvas', 'map', 'object', 'embed']):
                elem.decompose()
            title = soup.title.text if soup.title else '无标题'
            body = soup.body.get_text(separator='\n', strip=True) if soup.body else ''
            return title, body
        else:
            return None, f"请求失败，状态码: {resp.status_code}"
    except Exception as e:
        return None, f"请求异常: {str(e)}"

def generate_summary(url):
    web_title, web_body = fetch_page(url)

    if web_title is None:
        yield web_body # Error message
        return

    # Use ChatTongyi from langchain_community
    llm = ChatTongyi(model='qwen-plus', dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))

    # Format the prompt
    formatted_prompt = prompt.format(title=web_title, body=web_body)

    # Langchain's ChatModels expect a list of messages. We use HumanMessage.
    messages = [HumanMessage(content=formatted_prompt)]

    # Stream the response
    for chunk in llm.stream(messages):
        yield chunk.content

st.set_page_config(page_title="网页摘要生成助手 (LangChain)", page_icon="🔗", layout="wide")

st.write('## 网页摘要生成助手 (LangChain版)')
st.divider()

result = ''
col1, _, col2 = st.columns([3, 1, 6])

with col1:
    url_input = st.text_input(label='要生成摘要网址', placeholder='请输入完整的网址 (如: https://...)')
    button = st.button('确定', type='primary')

    if button and url_input.strip():
        with st.spinner("正在获取网页内容并生成摘要..."):
            result = generate_summary(url_input)

with col2:
    if result:
        st.write('网页摘要:')
        try:
            st.write_stream(result)
        except Exception as e:
            st.error(f"生成摘要时出错: {e}")
