"""techsupport


"""
import streamlit as st
from openai import OpenAI
import json
import logging
import sys

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are a technical expert specializing in Spring Boot microservices, PostgreSQL databases, and Linux systems. Your task is to analyze the provided log file snippet and diagnose the cause of the system outage. Your response should follow this JSON format:
{
  "rootCause": "",
  "escalateTo": "",
  "remediationSteps": []
}
Describe the root cause of the issue in the 'rootCause' field, providing a concise textual explanation based on the log file snippet.
Identify the best-suited role to address the issue in the 'escalateTo' field (Developer, DBA, Server Engineer, Network Engineer, DevOps Engineer).
List recommended steps for additional analysis or remediation in the 'remediationSteps' array, providing actionable text strings that could help resolve the incident or gather more information.
"""

# Log info and higher to the console
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

st.set_page_config(page_title="Tech Support Genius",
                   layout="centered",
                   initial_sidebar_state="collapsed",
                   menu_items=None)

with st.sidebar:
    openai_api_url = st.text_input(label="OpenAI API URL",
                                   key="openai_api_url",
                                   value="http://envision:11434/v1")
    openai_api_model_name = st.text_input(label="Model Name",
                                          key="openai_api_model_name",
                                          value="granite3.1-dense:8b")
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

st.title("💬 Tech Support Genius")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if prompt := st.chat_input("Enter stack trace, log snippet, or other details about the outage event"):

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    client = OpenAI(base_url=openai_api_url,
                    api_key="api-key")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    messages = [{"role": "assistant", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}]
    logging.info(f"Request: {messages}")

    response = client.chat.completions.create(model=openai_api_model_name,
                                              messages=messages,
                                              max_tokens=openai_max_tokens,
                                              temperature=openai_temperature)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})

    logging.info(f"Response: {msg}")

    with st.chat_message("assistant"):
        msg_obj = json.loads(msg)

        root_cause = msg_obj["rootCause"]
        escalate_to = msg_obj["escalateTo"]
        remediation_steps = msg_obj["remediationSteps"]

        st.write(f"**Root Cause:** {root_cause}")
        st.write(f"**Escalation Path:** {escalate_to}")
        st.write(f"**Remediation Steps:**")
        i = 0
        for step in remediation_steps:
            i += 1
            st.write(f"{i}. {step}")
