# 📚 Book RAG - Intelligent Novel Assistant

## Overview

**Book RAG** is a prototype intelligent reading assistant built using **Retrieval-Augmented Generation (RAG)** technology. The project aims to help readers understand Arabic novels and books more deeply by answering their questions about events, characters, and various meanings in the texts.

This system allows users to upload novels in PDF format, store them in a vector database, and then ask questions about specific words, ideas, events, or characters within those novels. The AI assistant provides contextual answers based on the actual content of the books.

### ✨ Key Features

- 📖 **Novel Upload & Storage**: Upload PDF files of novels and store them in a vector database
- 🤖 **Intelligent Chat**: Conversational system using Gemini AI to answer questions based on novel content
- 🔍 **Semantic Search**: Advanced search technology that understands Arabic context and finds appropriate answers
- 📑 **Source Documentation**: Display page numbers and excerpts used in the answers
- 👥 **Multi-Author Management**: Ability to add multiple authors and their novels
- 🌐 **Arabic Text Normalization**: Advanced text processing for better Arabic text matching

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Streamlit**: Interactive user interface framework
- **LangChain**: RAG framework and LLM integration
- **Google Gemini AI**: Large Language Model (LLM) and embeddings
- **ChromaDB**: Vector database for storing and retrieving text
- **PDFPlumber**: PDF text extraction library

---

## 📋 Requirements

- Python 3.11 or newer
- Google AI Studio account for API Key
- At least 4GB RAM
- Sufficient storage space for novels and database

---

## 🚀 Installation & Usage

### 1. Clone the Repository

```bash
git clone <repository-url>
cd book_rag
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

Or alternatively:

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**To obtain an API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in the `.env` file

### 5. Run the Application

```bash
streamlit run src/main.py
```

Or from the root directory:

```bash
cd c:/Users/DELL/OneDrive\ -\ AHU/Desktop/book_rag
streamlit run src/main.py
```

The application will automatically open in your browser at: `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Add an Author

1. Go to **Admin Panel** from the sidebar
2. In the **"Add Author"** tab, enter the author's name
3. Click **"Save Author"**

### Step 2: Upload a Novel

1. In the **"Upload Novel"** tab:
   - Select the author from the dropdown
   - Enter the novel title
   - Upload the novel's PDF file
2. Click **"Process and Store"**
3. Wait for the novel to be processed and split into chunks

### Step 3: Start Chatting

1. Go to **Chat** from the sidebar
2. Select the author and novel from the sidebar dropdowns
3. Start asking questions, such as:
   - "Who is the protagonist in this novel?"
   - "What happened in the first chapter?"
   - "What does this phrase mean: [text from the novel]"
   - "Who is the author of this novel?"

### Step 4: View Sources

- After each answer, you can click on **"📚 Sources"** to see:
  - Referenced page numbers
  - Excerpts from the original text

---

## 📁 Project Structure

```
book_rag/
├── src/
│   ├── __init__.py
│   ├── main.py                     # Main entry point
│   └── features/
│       ├── __init__.py
│       ├── admin/
│       │   ├── __init__.py
│       │   ├── ui.py              # Admin panel interface
│       │   └── ingest_service.py  # Novel processing and storage
│       └── chat/
│           ├── __init__.py
│           ├── ui.py              # Chat interface
│           └── rag_service.py     # RAG logic and querying
├── data/
│   ├── chroma_db/                 # Vector database
│   └── library.json               # Authors and novels metadata
├── .env                           # Environment variables (API Keys)
├── .gitignore
├── pyproject.toml                 # Project configuration and dependencies
└── README.md
```

---

## ⚠️ Important Notes

### This is a Prototype

- The project is in early development stage and needs improvements
- You may encounter some errors or inaccurate results
- Accuracy depends on PDF quality and text clarity
- This is an educational and experimental project

### Purpose

This system is designed to help readers:
- **Explain specific words or ideas** within novels or books
- Understand complex passages or concepts
- Get contextual explanations based on the actual content
- Find specific information quickly without reading the entire book

### Text Normalization

To improve search accuracy, Arabic texts are normalized by:
- Removing diacritics (vowel marks)
- Normalizing Alef variants (أ، إ، آ → ا)
- Normalizing Teh Marbuta and Heh (ة → ه)
- Normalizing Yaa and Alef Maksura (ى → ي)

### Re-uploading Novels

If you update the text processing logic, you may need to:
1. Delete the `data/chroma_db` folder
2. Re-upload novels from the Admin panel

---

## 🐛 Troubleshooting

### Module Import Errors

Make sure to run the application from the root directory:
```bash
streamlit run src/main.py
```

### API Key Error

Ensure:
- The `.env` file exists in the root directory
- The API Key from Google AI Studio is correct
- Variables are loaded using `python-dotenv`

### PDF Processing Issues

- Ensure the PDF file contains copyable text (not scanned images)
- Try extracting text manually to verify quality
- Use high-quality PDF files with clear text

### Inaccurate Search Results

- Try increasing the number of retrieved results (k) in `rag_service.py`
- Ensure text normalization is applied correctly
- Rephrase the question more clearly
- Re-upload the novel after improving text processing

---

## 🔮 Future Improvements

- [ ] Support additional file formats (EPUB, TXT, DOCX)
- [ ] Enhanced user interface design
- [ ] Long-term conversation memory
- [ ] Support for additional languages
- [ ] Advanced text analytics
- [ ] Answer rating system
- [ ] Export conversations feature
- [ ] Multi-document comparison
- [ ] Character and theme analysis tools

---

## 📄 License

This project is open-source and available for educational and development purposes.

---

## 👨‍💻 Developer

**Ibrahim Masa'deh**
- Email: ibrahim.masasdeh.prog@gmail.com

---

**Note**: This is an educational and experimental project. Please use it responsibly and respect intellectual property rights of novels and books. Always ensure you have the right to process and analyze the books you upload.
