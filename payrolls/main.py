import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from payrolls.models.database import init_db
from payrolls.routers import payrolls_endpoints

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8200",
    "http://127.0.0.1:8200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payrolls_endpoints.router, prefix="/payrolls")


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "payrolls.main:app", host="0.0.0.0", port=8300, log_level="debug", access_log=False, use_colors=False, workers=1
    )
