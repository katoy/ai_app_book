import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.globals import set_verbose, get_verbose
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_community.callbacks import get_openai_callback

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def init_page():
    st.set_page_config(
        page_title="Website Summarizer",
        page_icon="🤗"
    )
    st.header("Website Summarizer 🤗")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Select language and summary length below.")
        ]
        st.session_state.costs = []


def select_model():
    models = {
        "GPT-3.5": "gpt-3.5-turbo",
        "GPT-4": "gpt-4"
    }
    model = st.sidebar.radio("Choose a model:", tuple(models.keys()))
    model_name = models[model]
    return ChatOpenAI(temperature=0, model_name=model_name)


def select_language():
    language = st.sidebar.radio("Choose Language:", ("English", "Japanese"))
    set_verbose(language == "Japanese")
    return language


def get_url_input():
    url = st.text_input("URL: ", key="input")
    return url


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    try:
        with st.spinner("Fetching Content ..."):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except:
        st.write('something wrong')
        return None


def build_prompt(content, summary_length, language):
    prompt_text = {
        "English": "Please provide a concise summary of around",
        "Japanese": "以下の内容について、約"
    }
    lang_suffix = {
        "English": "characters.",
        "Japanese": "文字で要約してください。"
    }
    return f"{prompt_text[language]} {summary_length} {lang_suffix[language]}\n\n========\n\n{content[:2000]}"


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm.invoke(messages)
    return answer.content, cb.total_cost


def main():
    init_page()
    llm = select_model()
    init_messages()

    language = select_language()
    summary_length = st.sidebar.number_input("Set Summary Length:", min_value=100, max_value=800, value=300)

    container = st.container()
    response_container = st.container()

    with container:
        url = get_url_input()
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.write('Please input valid url')
            answer = None
        else:
            content = get_content(url)
            if content:
                prompt = build_prompt(content, summary_length, language)
                st.session_state.messages.append(HumanMessage(content=prompt))
                with st.spinner("ChatGPT is typing ..."):
                    answer, cost = get_answer(llm, st.session_state.messages)
                st.session_state.costs.append(cost)
            else:
                answer = None

    if answer:
        with response_container:
            st.markdown("## Summary")
            st.write(answer)
            summary_length_display = len(answer)
            st.markdown(f'<span style="font-size: 1.0em;">Length: {summary_length_display} characters</span>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("## Original Text")
            st.write(content)

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

if __name__ == '__main__':
    main()
