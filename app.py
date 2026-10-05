import os
import chainlit as cl
from src.loaders.policy_loader import PolicyLoader
from src.processors.text_splitter import PolicyTextSplitter
from src.vectorstore.faiss_store import FaissVectorStoreManager
from src.chatbot.qa_chain import QAChainBuilder
from src.config.settings import Settings

loader = PolicyLoader()
splitter = PolicyTextSplitter()
store_manager = FaissVectorStoreManager()

@cl.on_chat_start
async def on_chat_start():
    os.makedirs(Settings.POLICIES_DIR, exist_ok=True)
    
    if not os.path.exists(os.path.join(Settings.FAISS_INDEX_DIR, "index.faiss")):
        msg = cl.Message(content="⚙️ Scanning workspace layout for corporate manual documents...")
        await msg.send()
        
        documents = loader.load_pdfs()
        
        if not documents:
            msg.content = (
                "⚠️ No policy documents found in the `policies/` directory.\n\n"
                "👉 **Action Required:** Please drop your HR policy PDFs inside the `policies/` folder "
                "and restart this application."
            )
            await msg.update()
            return
            
        msg.content = "📦 Parsing and vectorizing documents via local embedding models..."
        await msg.update()
        
        chunks = splitter.split_documents(documents)
        vector_store = store_manager.create_and_save_store(chunks)
        
        msg.content = "✅ Policy Vector Knowledge Base generated successfully!"
        await msg.update()
    else:
        vector_store = store_manager.load_vector_store()

    rag_chain, retriever = QAChainBuilder.build_chain(vector_store)
    
    cl.user_session.set("rag_chain", rag_chain)
    cl.user_session.set("retriever", retriever)

    welcome_banner = (
        "### Corporate HR Policy Assistant 🏢\n"
        "Ask questions about company policies, leave rules, "
        "work-from-home guidelines, and the employee handbook.\n\n"
        "Answers are grounded in the uploaded policy documents and include source references."
    )
    await cl.Message(content=welcome_banner).send()


@cl.on_message
async def main(message: cl.Message):
    rag_chain = cl.user_session.get("rag_chain")
    retriever = cl.user_session.get("retriever")

    if not rag_chain or not retriever:
        await cl.Message(content="⚠️ System initialization failed.").send()
        return

    # Fetch source reference contexts natively
    retrieved_docs = retriever.invoke(message.content)

    # Invoke pipeline context using async wrapper execution standards
    ai_response = await cl.make_async(rag_chain.invoke)(message.content)

    source_elements = []
    text_references = []
    
    if retrieved_docs:
        text_references.append("\n\n### 📄 Verified Source Attributions:")
        for idx, doc in enumerate(retrieved_docs, start=1):
            file_name = os.path.basename(doc.metadata.get('source', 'Unknown Document'))
            page_num = doc.metadata.get('page', 0) + 1
            snippet = doc.page_content.strip()
            
            text_references.append(f"\n**[{idx}] Document:** {file_name} (Page {page_num})")
            source_elements.append(
                cl.Text(content=snippet, name=f"Source Chunk [{idx}]", display="inline")
            )

    final_output = ai_response + "".join(text_references)
    await cl.Message(content=final_output, elements=source_elements).send()