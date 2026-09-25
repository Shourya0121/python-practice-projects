from app.database import SessionLocal
from app.models.user import User
from app.utils.password import hash_password

db = SessionLocal()

try: 
    new_user = User(
        username="john",
        display_name="John",
        hashed_password=hash_password("john123")
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("User 2 created Successfully")
    print("User ID:", new_user.id)
    print("Username:", new_user.username)

except Exception as e:
    db.rollback()
    print("Error Creating User:", e)

finally:
    db.close()