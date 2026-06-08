from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.models.users import User
from app.core.security import decode_access_token
from app.crud.user import get_user_by_id

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(credentials.credentials)
    user_id = int(payload.get("sub"))
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return user
