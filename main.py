import anthropic
import os
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

SYSTEM = "You are Ralph from Lord of the Flies, base your speech only on what he would do and how he would say it. Do not describe the characters actions or movements, only dialogue."

history = []

while True:
    user_input = input("").strip()
    if user_input == "exit":
        break

    history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=200,
        system=SYSTEM,
        messages=history,
    )

    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})

    print(f"\nRalph: {reply}\n")
