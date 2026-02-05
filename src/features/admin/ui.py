import streamlit as st          # type: ignore
import os
import json
from src.features.admin.ingest_service import process_and_save_document

# JSON's path to store novels and authors

LIBRARY_FILE = os.path.join("data", "library.json")

def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return {}
    
    with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_library(library_data):
    os.makedirs("data", exist_ok=True)

    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        json.dump(library_data, f, ensure_ascii=False, indent=4)

def render_admin_panel():
    """
    called in main.py
    draws the admin panel UI
    """

    st.header("🛠️ لوحة التحكم - إدارة الروايات")

    library = load_library()

    tab1, tab2 = st.tabs(["إضافة مؤلف", "رفع رواية"])

    # Tab 1: Add Author

    with tab1:
        new_author = st.text_input("اسم المؤلف")
        if st.button("حفظ مؤلف"):
            if new_author and new_author not in library:
                library[new_author] = []
                save_library(library)
                st.success(f"تم حفظ المؤلف: {new_author}")
                st.rerun()
            
            elif new_author in library:
                st.warning("المؤلف موجود مسبقاً")

    # Tab 2: Upload Novel
    with tab2:
        authors = list(library.keys())
        if not authors:
            st.info("يرجى إضافة مؤلف أولاً في تبويب 'إضافة مؤلف'")
        
        else:
            selected_author = st.selectbox("اختر المؤلف", authors)
            novel_title = st.text_input("عنوان الرواية")
            uploaded_file = st.file_uploader("ملف الرواية PDF", type=["pdf"])

            if st.button("معالجة وتخزين"):
                if uploaded_file and novel_title:

                    with st.spinner("جاري قراءة الملف، تقسيمه، وتخزينه في قاعدة البيانات..."):
                        num_chunks = process_and_save_document(uploaded_file, selected_author, novel_title)

                        if novel_title not in library[selected_author]:
                            library[selected_author].append(novel_title)
                            save_library(library)
                    
                    st.success(f"تمت العملية بنجاح! تم تخزين {num_chunks} فقرة.")
                else:
                    st.error("يرجى التأكد من جميع الحقول")