from fastapi import APIRouter,HTTPException
from app.db.database import sessionDep
from app.db.models import User
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

router=APIRouter()

@router.post("/signup")
def signUp(user:User,session:sessionDep):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError as e:
        session.rollback()

        # Check if it's the unique violation on email
        if isinstance(e.orig, UniqueViolation):
            return HTTPException(
                status_code=400,
                detail="Email already exists"
            )
        
        # Some other DB error
        return HTTPException(
            status_code=500,
            detail="Database error"
        )
        
    