import os
import re
from langchain_community.vectorstores import Chroma        # type: ignore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI  # type: ignore
from langchain_core.prompts import ChatPromptTemplate             # type: ignore
from langchain_core.output_parsers import StrOutputParser          # type: ignore
from langchain_core.runnables import RunnablePassthrough          # type: ignore


CHROMA_PATH = os.path.join("data", "chroma_db")


def normalize_arabic(text):
    """
    Normalize Arabic text for better matching
    """
    if not text:
        return ""
    
    # Remove diacritics
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
    
    # Normalize alef variants
    text = re.sub(r'[إأآا]', 'ا', text)
    
    # Normalize teh marbuta
    text = re.sub(r'ة', 'ه', text)
    
    # Normalize yaa
    text = re.sub(r'ى', 'ي', text)
    
    return text


def get_rag_response(question, author_name, novel_title):
    """
    takes question and novel_title
    searches in chroma db
    sends context to llm
    """

    # Normalize the question for better search
    normalized_question = normalize_arabic(question)

    embeddings_function = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings_function,
    )

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            'k': 5,
            'filter': {
                "$and": [
                    {"author": author_name},
                    {"novel": novel_title}
                ]
            }
        }
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
    )

    template = """أنت ناقد أدبي وخبير في الأدب العربي.

**معلومات الرواية:**
- العنوان: {novel_title}
- المؤلف: {author_name}

مهمتك هي الإجابة على سؤال المستخدم. إذا كان السؤال عن معلومات أساسية (المؤلف، العنوان، إلخ)، أجب مباشرة من المعلومات أعلاه.
إذا كان السؤال عن محتوى الرواية، استخدم السياق المقتبس أدناه للإجابة.
    
    القواعد:
    1. استخدم لغة عربية سليمة وسهلة الفهم.
    2. إذا سُئلت عن المؤلف أو الكاتب، أجب: "مؤلف رواية {novel_title} هو {author_name}."
    3. للأسئلة عن المحتوى، استشهد بالأحداث من السياق المقدم.
    4. إذا كانت الإجابة عن المحتوى غير موجودة في السياق، قل: "للأسف، هذا الجزء لم يذكر في السياق المتاح من الرواية."
    5. حاول أن تذكر رقم الصفحة إن كان متعلقاً بمحتوى الرواية.

    السياق المقتبس من الرواية:
    {context}

    سؤال المستخدم:
    {question}

    الإجابة:
    """

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join([
            f"[الصفحة {doc.metadata.get('page', 'غير معروف')}]: {doc.page_content}"
            for doc in docs
        ])

    # Create the RAG chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "author_name": lambda _: author_name,
            "novel_title": lambda _: novel_title,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Get the answer - use normalized question for retrieval
    answer = rag_chain.invoke(normalized_question)
    
    # Get source documents - use normalized question
    source_docs = retriever.invoke(normalized_question)

    return {
        "answer": answer,
        "sources": source_docs
    }