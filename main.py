from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import item  
import os
import uvicorn

# FastAPI instance
app = FastAPI(title="Item CRUD API", version="1.0")

# CORS configuration
origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

# Root endpoint
@app.get("/")
async def get_app_details():
    return {"message": "FastAPI is running..."}

# Include the item router
app.include_router(item.router, prefix="/api", tags=["Items"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
