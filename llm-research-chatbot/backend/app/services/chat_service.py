# backend/app/services/chat_service.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from ..config import MODEL_CONFIG

class ChatService:
    def __init__(self, pages):
        self.llm = None
        self.retrieval_chain = None
        self.memory = None
        self.pages = pages
        self.initialize_service()

    def initialize_service(self):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_CONFIG["llm_model"],
            temperature=MODEL_CONFIG["temperature"],
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        # Initialize embeddings and vector store
        embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_CONFIG["embedding_model"]
        )
        vector_store = FAISS.from_documents(self.pages, embeddings)
        retriever = vector_store.as_retriever()

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )

        # Create prompt template and chains
        prompt_template = ChatPromptTemplate.from_template("""
        Use the following context to answer the user's questions. Keep the conversation history in mind for continuity.

        <context>
        {context}
        </context>

        Conversation History:
        {history}

        User: {input}
        Assistant:
        """)

        document_chain = create_stuff_documents_chain(self.llm, prompt_template)
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)

    async def get_response(self, message: str) -> str:
        response = self.retrieval_chain.invoke({
            "context": "You are an expert summarizing and explaining concepts, methodologies, "
                "and findings from research papers related to Large Language Models (LLMs). "
                "You can provide insights into topics such as model architectures, "
                "training techniques, evaluation metrics, comparisons between models, "
                "and their real-world applications.",
            "input": message,
            "history": self.memory.load_memory_variables({})["history"]
        })

        # Update memory
        self.memory.save_context(
            inputs={"input": message},
            outputs={"output": response["answer"]}
        )

        return response["answer"]