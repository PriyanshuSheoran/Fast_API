from fastapi import FastAPI
from app.database import engine, Base
from app.admin_setup import create_admin
from app.routes import books, users, auth, admin  # ✅ Import admin router

app = FastAPI()


Base.metadata.create_all(bind=engine)


create_admin()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])  # ✅ Add admin routes

@app.get("/")
def root():
    return {"message": "Welcome to the Library Management System"}
