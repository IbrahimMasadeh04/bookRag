import streamlit as st               # type: ignore
import os
import json

from src.features.chat.rag_service import get_rag_response

LIBRARY_FILE = os.path.join("data", "library.json")


def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return {}
    
    with open(LIBRARY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_chat_page():
    """
    Main function to render the Chat Interface
    """

    st.title("مساعد القراءة الذكي")

    # --- 1. Sidebar: Context Selection ---
    library = load_library()

    if not library:
        st.warning("!المكتبة فارغة! الرجاء الذهاب للوحة التحكم وإضافة روايات أولاً.")
        return
    
    st.sidebar.header("إعدادات المحادثة")

    selected_author = st.sidebar.selectbox(
        "اختر المؤلف: ",
        options=list(library.keys())
    )

    available_novels = library.get(selected_author, [])

    if not available_novels:
        st.warning("!لا توجد روايات لهذا المؤلف! الرجاء الذهاب للوحة التحكم وإضافة روايات أولاً.")
        return
    
    selected_novel = st.sidebar.selectbox(
        "اختر الرواية: ",
        options=available_novels
    )

    # add a Clear Chat button

    if st.sidebar.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"أنت تسأل الآن عن: **{selected_novel}**")

    # --- 2. Chat History Management ---
    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # If there are sources stored in the history, display them
            if "sources" in message:
                with st.expander("📚 المصادر (أرقام الصفحات)"):
                    for src in message["sources"]:
                        st.caption(f"- صفحة {src.get('page', 'غير معروف')}: ...{src.get('preview', '')}...")

    
    # --- 3. User Input & Processing ---
    if prompt := st.chat_input("اسأل عن حدث، شخصية، أو معنى في الرواية..."):
        # a. Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # b. Generate AI response
        with st.chat_message("assistant"):
            with st.spinner(f"جاري البحث في '{selected_novel}'..."):
                try:
                    response_data = get_rag_response(prompt, selected_author, selected_novel)
                    
                    answer_text = response_data['answer']
                    source_docs = response_data["sources"]

                    # process source for cleaner display
                    formatted_sources = []

                    for doc in source_docs:
                        formatted_sources.append(
                            {
                                "page": doc.metadata.get("page", "?"),
                                "preview": doc.page_content[:50]
                            }
                        )

                    st.markdown(answer_text)

                    # display sources in an expander (collapsible)
                    if formatted_sources:
                        with st.expander("📚 المصادر (أرقام الصفحات)"):
                            for src in formatted_sources:
                                st.caption(f"📄 **صفحة {src['page']}**")
                    

                    # add to history
                    st.session_state.messages.append(
                        {
                            "role": "assistant", 
                            "content": answer_text,
                            "sources": formatted_sources,
                        }
                    )

                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")