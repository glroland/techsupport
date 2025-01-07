"""techsupport


"""
import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_url = st.text_input(label="OpenAI API URL",
                                   key="openai_api_url",
                                   value="http://envision:8000/v1")
    openai_api_model_name = st.text_input(label="Model Name",
                                          key="openai_api_model_name",
                                          value="meta-llama/Meta-Llama-3.1-8B-Instruct")
    openai_max_tokens = st.number_input(label="Max Tokens",
                                        min_value=1,
                                        max_value=10000,
                                        value=1000,
                                        step=10)
    openai_temperature = st.number_input(label="Temperature",
                                         min_value=0.0,
                                         max_value=1.0,
                                         value=0.8,
                                         step=0.1)


st.title("💬 techsupport Agent")

system_prompt_showhide = st.empty()
system_prompt_container = system_prompt_showhide.container()
system_prompt = system_prompt_container.text_area(label="System Prompt",
                key="system_prompt",
                value="You are a helpful sales agent for a shoe store, who is always " +
                      "positive and never participates in negative conversations. " +
                      "Only participate in conversations related to shoes and the store.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": system_prompt}]

if prompt := st.chat_input():

    system_prompt_showhide.empty()
    if 'system_prompt' in st.session_state and st.session_state.system_prompt is True:
        st.session_state.system_prompt = True

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    client = OpenAI(base_url=openai_api_url,
                    api_key="api-key")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=openai_api_model_name,
                                              messages=st.session_state.messages,
                                              max_tokens=openai_max_tokens,
                                              temperature=openai_temperature)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
