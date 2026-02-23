import anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

character = st.text_input("Who do you want to speak with?")

if character:
    SYSTEM = f"You are {character} from Lord of the Flies. Only dialogue, no action descriptions. 2-3 complete sentences, always finish on a full stop."

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input(f"Speak to {character}..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            system=SYSTEM,
            messages=st.session_state.history,
        )
        reply = response.content[0].text
        st.session_state.history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
The chat input only appears once a character name has been typed, which is the behaviour you were after. Your original logic is all still there — just restructured to work with how Streamlit runs.Remove the profile pictures1:44 PMReplace the with st.chat_message(...) blocks with plain st.write() calls:
pythonimport anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

character = st.text_input("Who do you want to speak with?")

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
        st.write(f"**{character}:** {reply}")How can I now implement the 4-way conversation as an additional feature1:56 PMAdd a second page using Streamlit's st.sidebar to switch modes, then implement the debate logic we discussed earlier:
pythonimport anthropic
import streamlit as st

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

SYSTEMS = {
    "Ralph":  "You are Ralph from Lord of the Flies. Short sentences, plain words, 'd'you', 'rotten'. Care about rules and the fire. Frustrated and tired. Only dialogue, no actions. 2-3 complete sentences, always finish on a full stop.",
    "Jack":   "You are Jack Merridew from Lord of the Flies. Jabbing short sentences, sneer, contemptuous. Hunt is everything. Only dialogue, no actions. 2-3 complete sentences, always finish on a full stop.",
    "Piggy":  "You are Piggy from Lord of the Flies. Drop your h's, working class, invoke your auntie. Frustrated at being ignored. Only dialogue, no actions. 2-3 complete sentences, always finish on a full stop.",
    "Simon":  "You are Simon from Lord of the Flies. Quiet, halting, trail off with '...'. Gentle and strange. Only dialogue, no actions. 2-3 complete sentences, always finish on a full stop.",
}

# Sidebar mode switcher
mode = st.sidebar.radio("Mode", ["Single Character", "4-Way Debate"])

# ── Single character mode ──────────────────────────────────────────────────
if mode == "Single Character":
    if "history" not in st.session_state:
        st.session_state.history = []

    character = st.text_input("Who do you want to speak with?")

    if character:
        system = SYSTEMS.get(character, f"You are {character} from Lord of the Flies. Only dialogue, no action descriptions. 2-3 complete sentences, always finish on a full stop.")

        for msg in st.session_state.history:
            label = character if msg["role"] == "assistant" else "You"
            st.write(f"**{label}:** {msg['content']}")

        if prompt := st.chat_input(f"Speak to {character}..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            st.write(f"**You:** {prompt}")

            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=500,
                system=system,
                messages=st.session_state.history,
            )
            reply = response.content[0].text
            st.session_state.history.append({"role": "assistant", "content": reply})
            st.write(f"**{character}:** {reply}")

# ── 4-way debate mode ──────────────────────────────────────────────────────
else:
    st.title("4-Way Debate")

    if "debate_history" not in st.session_state:
        st.session_state.debate_history = []

    def build_messages_for(character, history, topic):
        messages = [{"role": "user", "content": f"The topic being debated is: {topic}. Respond in character, react to what the others just said."}]
        for entry in history:
            if entry["character"] == character:
                messages.append({"role": "assistant", "content": entry["content"]})
            else:
                messages.append({"role": "user", "content": f"{entry['character']}: {entry['content']}"})
        return messages

    def run_round(topic):
        for character in ["Ralph", "Jack", "Piggy", "Simon"]:
            messages = build_messages_for(character, st.session_state.debate_history, topic)
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=500,
                system=SYSTEMS[character],
                messages=messages,
            )
            reply = response.content[0].text
            st.session_state.debate_history.append({"character": character, "content": reply})

    # Display history
    for entry in st.session_state.debate_history:
        st.write(f"**{entry['character']}:** {entry['content']}")

    # Topic input — only shown if no debate started yet
    if not st.session_state.debate_history:
        topic = st.text_input("Enter a debate topic:")
        if st.button("Start Debate") and topic:
            st.session_state.debate_topic = topic
            run_round(topic)
            st.rerun()

    # Continue and clear buttons once debate is running
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Round"):
                run_round(st.session_state.debate_topic)
                st.rerun()
        with col2:
            if st.button("Clear"):
                st.session_state.debate_history = []
                st.rerun()
