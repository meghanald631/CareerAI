
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.token import SECRET_KEY, ALGORITHM


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    print("STEP 1: Authorization received")

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        print("STEP 2: Token decoded:", payload)

        user_id = int(payload.get("sub"))
        print("STEP 3: User ID:", user_id)

        current_user = db.query(User).filter(
            User.id == user_id
        ).first()

        print("STEP 4: Database lookup completed")

        if current_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return current_user

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")