import os
import pdfplumber                                                       # type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter     # type: ignore
from langchain_google_genai import GoogleGenerativeAIEmbeddings         # type: ignore
from langchain_community.vectorstores import Chroma                     # type: ignore
from langchain_core.documents import Document                           # type: ignore              

CHROMA_PATH = os.path.join("data", "chroma_db")

def clean_arabic_text(text):
    """
    clean arabic words from excessive whitespaces
    """

    if not text:
        return ""
    
    text = " ".join(text.split())
    return text

########################################################

def process_and_save_document(uploaded_file, athor_name, novel_title):
    """
    - read file
    - chunk text
    - save chunks
    """

    print(f"Ingesting document {novel_title}")

    full_text = ""
    docs = []

    with pdfplumber.open(uploaded_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text:
                clean_text = clean_arabic_text(text)
                
                doc = Document(
                    page_content=clean_text,
                    metadata={
                        'page': i + 1, 
                        'author': athor_name,
                        'novel': novel_title
                    }
                )

                docs.append(doc)
        
        print(f"Extracted {len(docs)} pages.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", ".", "،", " ", ""], # Arabic punctuation included; order matters
        )

        chunks = text_splitter.split_documents(docs)
        print(f"Split into {len(chunks)} chunks.")

        embedding_function = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )

        # save to chroma

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function,
            persist_directory=CHROMA_PATH
        )

        vector_db.persist()

    print(f"Document {novel_title} ingested and saved to vector store.")
    return len(chunks)

