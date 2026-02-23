import anthropic
import os
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

character = st.text_input("Who do you want to speak with? ")

SYSTEM = "You are " + character + " from Lord of the Flies, base your speech only on what he would do and how he would say it. Do not describe the characters actions or movements, only dialogue. Do not cut off, keep responses within the limit of 500 tokens."

history = []

while True:
    user_input = st.text_input("").strip()
    if user_input == "exit":
        break

    history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=500,
        system=SYSTEM,
        messages=history,
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})

    st.write(character + ": " + reply)




