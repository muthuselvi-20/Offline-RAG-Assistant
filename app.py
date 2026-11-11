import streamlit as st

from main import (
    process_file_bytes,
    ask_question
)

from history import (
    create_session,
    get_history,
    clear_history
)

from vectordb import get_total_chunks


# PAGE CONFIGURATION

st.set_page_config(

    page_title="Offline RAG Assistant",

    page_icon="📚",

    layout="wide"

)


st.title("📚 Offline RAG Document Assistant")

st.caption(
    "Chat with your PDF, DOCX and image documents."
)


# CREATE SESSION

if "session_id" not in st.session_state:

    st.session_state.session_id = create_session()


session_id = st.session_state.session_id


# SIDEBAR

with st.sidebar:

    st.header("Knowledge Base")

    st.metric(
        "Stored Chunks",
        get_total_chunks()
    )

    st.divider()

    st.subheader("Upload Documents")

    uploaded_files = st.file_uploader(

        "Select documents",

        type=[
            "pdf",
            "docx",
            "png",
            "jpg",
            "jpeg",
            "bmp",
            "tiff",
            "webp"
        ],

        accept_multiple_files=True

    )

    if st.button(
        "Process Documents",
        disabled=not uploaded_files
    ):

        for uploaded_file in uploaded_files:

            try:

                with st.spinner(
                    f"Processing {uploaded_file.name}..."
                ):

                    result = process_file_bytes(

                        uploaded_file.name,

                        uploaded_file.getvalue()

                    )

                st.success(

                    f"{result['filename']} processed. "

                    f"{result['chunks']} chunks stored."

                )

            except Exception as error:

                st.error(
                    str(error)
                )

        st.rerun()

    st.divider()

    if st.button("New Chat"):

        st.session_state.session_id = create_session()

        st.rerun()

    if st.button("Clear Current Chat"):

        clear_history(session_id)

        st.rerun()


# CHAT HISTORY

st.subheader("Conversation")


chat_history = get_history(session_id)


for message in chat_history:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# USER INPUT

question = st.chat_input(
    "Ask something about your documents..."
)


if question:

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                result = ask_question(

                    question,

                    session_id

                )

                st.markdown(
                    result["answer"]
                )

                st.markdown("### Sources")

                seen = set()

                for source in result["sources"]:

                    source_name = source["source"]

                    page = source["page"]

                    if page != -1:

                        label = (
                            f"{source_name} — Page {page}"
                        )

                    else:

                        label = source_name

                    if label not in seen:

                        st.write(f"- {label}")

                        seen.add(label)

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    st.rerun()