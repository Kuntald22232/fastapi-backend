from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import items   # <-- backend থেকে items router import
import os
import uvicorn

app = FastAPI(title="Item CRUD API", version="1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_app_details():
    return {"message": "FastAPI is running..."}

# include router
app.include_router(items.router, prefix="/api", tags=["Items"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
