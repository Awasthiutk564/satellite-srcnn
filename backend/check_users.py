from app.db.session import SessionLocal
from app.db.base import Base # This imports User, Image, Result
from app.db.models.user import User

db = SessionLocal()
try:
    users = db.query(User).all()
    print(f"Total users in DB: {len(users)}")
    for u in users:
        print(f"- {u.email} ({u.full_name})")
except Exception as e:
    print(f"Error checking users: {e}")
finally:
    db.close()
