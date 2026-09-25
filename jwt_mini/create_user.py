from app.database import SessionLocal
from app.models.user import User
from app.utils.password import hash_password


db = SessionLocal()

try:
    new_user = User(
        username="shourya",
        display_name="Shourya",
        hashed_password=hash_password("python123")
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("User created successfully!")
    print("User ID:", new_user.id)
    print("Username:", new_user.username)

except Exception as e:
    db.rollback()
    print("Error creating user:", e)

finally:
    db.close()