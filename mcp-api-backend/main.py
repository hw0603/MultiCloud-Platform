from fastapi import FastAPI
from api.v1.route import api_router


app = FastAPI(
    title="Multi Cloud Platform API",
    description="퍼블릭 기반 멀티클라우드 플랫폼 API 서버",
    version="1.0.0",
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def main():
    return {"message": "API Server main page"}
