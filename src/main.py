import streamlit as st                # type: ignore
import os
import sys
from dotenv import load_dotenv        # type: ignore

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features.admin.ui import render_admin_panel
from src.features.chat.ui import render_chat_page
load_dotenv()

st.set_page_config(
    page_title="مكتبة الروايات",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.sidebar.title("التنقل")
    page = st.sidebar.radio("اذهب الى: ", ["المحادثة (chat)", "لوحة التحكم (Admin)"])

    if page == "لوحة التحكم (Admin)":
        render_admin_panel()
    else:
        render_chat_page()

if __name__ == "__main__":
    main()