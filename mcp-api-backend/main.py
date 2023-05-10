from fastapi import FastAPI
from api.v1.route import api_router
from db.session import async_engine, engine
from db.model import user_model, aws_cloudwatch_model, stack_model


app = FastAPI(
    title="Multi Cloud Platform API",
    description="퍼블릭 기반 멀티클라우드 플랫폼 API 서버",
    version="1.0.0",
)
app.include_router(api_router, prefix="/api/v1")


# DB 테이블 생성
# user_model.Base.metadata.create_all(bind=engine)
# aws_cloudwatch_model.Base.metadata.create_all(bind=engine)
@app.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.create_all)
        await conn.run_sync(aws_cloudwatch_model.Base.metadata.create_all)
        await conn.run_sync(stack_model.Base.metadata.create_all)


@app.get("/")
def main():
    return {"message": "API Server main page"}
