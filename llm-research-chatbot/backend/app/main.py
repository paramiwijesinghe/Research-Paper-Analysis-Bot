
# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.chat import ChatMessage, ChatResponse
from .services.chat_service import ChatService
from .utils.pdf_loader import load_pdf
from .config import API_CONFIG, DATA_DIR

app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"]
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_service = None

@app.on_event("startup")
async def startup_event():
    global chat_service
    # Load PDF
    pdf_path = DATA_DIR / "research_paper.pdf"
    pages = load_pdf(pdf_path)
    # Initialize chat service
    chat_service = ChatService(pages)

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    if not chat_service:
        raise HTTPException(status_code=500, detail="Chat service not initialized")
    
    try:
        response = await chat_service.get_response(message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

