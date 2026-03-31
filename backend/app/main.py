from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .routes import study_items, reviews, recommendations

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Study Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(study_items.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message": "Study Planner API is running"}
