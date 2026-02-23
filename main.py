import anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

character = st.selectbox("Who do you want to speak with?", ["Ralph", "Jack", "Piggy", "Simon"])

if "current_character" not in st.session_state or st.session_state.current_character != character:
    st.session_state.history = []
    st.session_state.current_character = character

SYSTEM = f"""You are {character} from Lord of the Flies. Base your speech only on 
how they would actually talk. Only dialogue — no action descriptions or stage directions. 
Respond in 2-3 complete sentences. Always finish on a full stop."""

if character:
    for msg in st.session_state.history:
        role_label = character if msg["role"] == "assistant" else "You"
        with st.wriote(msg["role"]):
            st.write(f"{role_label}: {msg['content']}")

    if prompt := st.chat_input(f"Speak to {character}..."):
        with st.write("user"):
            st.write(f"You: {prompt}")
        st.session_state.history.append({"role": "user", "content": prompt})

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=SYSTEM,
            messages=st.session_state.history,
        )
        reply = response.content[0].text
        st.session_state.history.append({"role": "assistant", "content": reply})

        with st.write("assistant"):
            st.write(f"{character}: {reply}")
        st.session_state.history.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(f"{character}: {reply}")
