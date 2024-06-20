from fastapi import FastAPI
from app.core.db import engine
from app.models.db.models import Base

from app.api.endpoints import api_router


app = FastAPI()

app.include_router(api_router)


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")


@app.on_event("startup")
async def startup_event():
    await create_all_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
