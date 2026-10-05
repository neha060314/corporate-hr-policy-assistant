from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import Settings
from src.prompts.hr_prompt import HRPromptTemplate

class QAChainBuilder:
    
    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def build_chain(vector_store):
        # Initializing modern 2026 consolidated ChatGoogleGenerativeAI object wrapper
        llm = ChatGoogleGenerativeAI(
            model=Settings.MODEL_NAME,
            google_api_key=Settings.GOOGLE_API_KEY,
            temperature=0.1
        )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        prompt = HRPromptTemplate.get_prompt()
        
        # Declarative LCEL Pipeline Construction
        rag_chain = (
            {
                "context": retriever | QAChainBuilder.format_docs, 
                "question": RunnablePassthrough()
            }
            | prompt 
            | llm 
            | StrOutputParser()
        )
        
        return rag_chain, retriever