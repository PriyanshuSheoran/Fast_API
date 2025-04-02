import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Default fallback
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")  # You can set a default email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db: Session = SessionLocal()
    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
    
    if not admin:
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)  
        admin_user = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,  
            password_hash=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("✅ Admin user created successfully!")
    else:
        print("✅ Admin user already exists.")
    db.close()


create_admin()

