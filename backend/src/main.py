from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.auth_route import router as auth_router
from route.item_route import router as item_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 경우 ["http://localhost:3000"]로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(item_router)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with CORS!"}

@app.get("/hi")
async def hi():
    return {"message": "우꾸우꾸"}
