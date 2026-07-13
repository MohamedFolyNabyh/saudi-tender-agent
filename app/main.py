from fastapi import FastAPI

from app.routers.upload_router import router as upload_router
from app.routers.chat_router import router as chat_router


app = FastAPI(
    title="Saudi Tender Agent",
    description="AI Agent for Saudi Government Tenders",
    version="1.0.0"
)


app.include_router(upload_router)

app.include_router(chat_router)


@app.get("/")
async def root():

    return {
        "message": "Saudi Tender Agent API"
    }