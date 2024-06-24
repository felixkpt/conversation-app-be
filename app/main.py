from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import health, category, subcategory, conversation, audio, interview, auto_page_builder
from app.models.database import setup_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(conversation.router)
app.include_router(audio.router)
app.include_router(interview.router)
app.include_router(auto_page_builder.router)


@app.get("/setup-database")
async def set_database():
    setup_database()
