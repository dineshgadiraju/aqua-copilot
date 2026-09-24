import streamlit as st
import requests


def ask_assistant(
    api_url,
    pond_name,
    question,
):
    """
    Send a pond-specific question to the backend AI assistant.
    """

    try:
        response = requests.get(
            f"{api_url}/ponds/{pond_name}/assistant",
            params={
                "question": question,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        return {
            "status": "ERROR",
            "message": str(error),
        }


def render_pond_assistant(
    api_url,
    pond_name,
):
    """
    Render the Aqua Copilot AI Pond Assistant.
    """

    st.subheader("🤖 AI Pond Assistant")

    st.caption(
        "Ask questions about pond health, alerts, "
        "water quality, risk, and forecasts."
    )

    # Create separate chat history for each pond
    history_key = f"assistant_history_{pond_name}"

    if history_key not in st.session_state:
        st.session_state[history_key] = []

    # Display previous messages
    for message in st.session_state[history_key]:

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

    # User question
    question = st.chat_input(
        f"Ask about {pond_name}..."
    )

    if question:

        # Save user message
        st.session_state[history_key].append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Ask backend
        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing pond data..."
            ):

                result = ask_assistant(
                    api_url,
                    pond_name,
                    question,
                )

            if result.get("status") == "OK":

                answer = result.get(
                    "answer",
                    "No answer was returned.",
                )

                st.markdown(answer)

                st.session_state[
                    history_key
                ].append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            else:

                error_message = result.get(
                    "message",
                    "AI assistant is currently unavailable.",
                )

                st.error(error_message)