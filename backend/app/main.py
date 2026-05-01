from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import domain as models
from app.database import engine
from app.routers import auth, projects, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def health_check():
    return {"status": "ok", "app": "Team Task Manager"}
