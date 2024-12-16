from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.model.users import Waitlist, User
from email_validator import validate_email, EmailNotValidError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Depends, APIRouter
from app.utils.misc import get_sqlite_session, hash_password, verify_password
from app.utils.auth_flow_manager import create_jwt_access_token
router = APIRouter()

@router.post("/signup")
def signup_user(
    email: str,
    first_name: str,
    last_name: str,
    country: str,
    password: str,
    session: Session = Depends(get_sqlite_session)
):
    """
    Signup endpoint for non-Google users.
    """
    # Check if user already exists
    if session.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        country=country,
        password=hashed_password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User signed up successfully", "user_email": new_user.email}

@router.post("/subscribe-waitlist/")
async def subscribe_waitlist(email: str,
                             session: Session=Depends(get_sqlite_session)):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    existing_user = session.query(Waitlist).filter(Waitlist.email == email).first()

    if existing_user:
        return JSONResponse(content={"error": "Email already exists."},
                            status_code=400)

    # Insert the new email into the database
    new_user = Waitlist(email=email)
    session.add(new_user)
    try:
        session.commit()
        return JSONResponse(content={"message": "User added successfully!"},
                            status_code=201)
    except Exception as e:
        session.rollback()
        return JSONResponse(content={"error": f"Unexpected error: {e}"},
                            status_code=500)


#@router.post("/login")
#def login_user(email: str, password: str,
#               session: Session = Depends(get_sqlite_session)):
#    """Login endpoint for non-Google users."""
#    user = session.query(User).filter(User.email == email).first()
#    if not user or not verify_password(password, user.password):
#        raise HTTPException(status_code=400, detail="Invalid email or password")
#
#    access_token = create_jwt_access_token(data={"sub": user.email})
#    return {"access_token": access_token}
