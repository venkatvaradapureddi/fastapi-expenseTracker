from fastapi import FastAPI
from db import Base,engine
from  routes import auth_routes,expenses_routes
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
origins = [
    "http://localhost:3000",   # for CRA
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # for Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ✅ specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # ✅ allow all methods (POST, GET, etc.)
    allow_headers=["*"],            # ✅ allow all headers (like Content-Type)
)
Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router,prefix="")
app.include_router(expenses_routes.router,prefix="")