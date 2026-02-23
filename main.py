import anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

character = st.selectbox("Who do you want to speak with?", ["Ralph", "Simon", "Jack", "Piggy"])

if character:
    SYSTEM = f"You are {character} from Lord of the Flies. Only dialogue, no action descriptions. 2-3 complete sentences, always finish on a full stop."

    for msg in st.session_state.history:
        label = character if msg["role"] == "assistant" else "You"
        st.write(f"**{label}:** {msg['content']}")

    if prompt := st.chat_input(f"Speak to {character}..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.write(f"**You:** {prompt}")

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=SYSTEM,
            messages=st.session_state.history,
        )
        reply = response.content[0].text
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.write(f"**{character}:** {reply}")

