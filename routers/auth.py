# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from database import get_db
# import models
# from schemas import UserCreate
# from user import get_user_by_email, get_user_by_username
# from passwordManager import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# from datetime import datetime, timedelta

# from typing import Annotated, Union
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# # dependency.py script
# from jose import jwt
from jose.exceptions import JOSEError
# from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


# router = APIRouter(prefix="/auth")

# def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
#     user = get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user

# @router.post("/user-registration", tags=['User Registration'])
# async def user_registration(userData: UserCreate, db: Session = Depends(get_db)):
#     # Check if the email is already registered
#     email_exists = get_user_by_email(db, userData.email)
#     if email_exists:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

#     # Check if the username is already taken
#     username_exists = get_user_by_username(db, userData.username)
#     if username_exists:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

#     # Create a new user with the provided data
#     hash_password = get_password_hash(userData.plainpassword)
#     user = models.User(username=userData.username, email=userData.email,password=hash_password, first_name=userData.firstname, last_name=userData.lastname)
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # # Generate an access token for email confirmation
#     # token_data = {"sub": user.id}
#     # #access_token = create_access_token(token_data)

#     # Send the access token to the user's email for confirmation
#     #send_confirmation_email(user.email, access_token)

#     return {"message": "User Created Successfully"}


# @router.post("/login", tags=["Login"])
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}



####Here is the new code####
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from models import User, LoginHistory
from schemas import UserCreate
from sqlalchemy.orm import Session
from models.user import get_user_by_email, get_user_by_username
from database import get_db
from utils.loginHistory import createLoginHistory

router = APIRouter(prefix="/auth")

security = HTTPBearer()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_token(credentials: HTTPAuthorizationCredentials= Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if token is None:
            raise credentials_exception
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            user = get_user_by_username(db, username)
            if user is None:
                raise credentials_exception
            return user
        except JWTError:
            raise credentials_exception
    except HTTPException as e:
        raise e
    
# async def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
#     """
#         Function that is used to validate the token in the case that it requires it
#     """
#     token = credentials.credentials

#     try:
#         payload = jwt.decode(token, key='secret', options={"verify_signature": False,
#                                                            "verify_aud": False,
#                                                            "verify_iss": False})
#         print("payload => ", payload)
#     except JOSEError as e:  # catches any exception
#         raise HTTPException(
#             status_code=401,
#             detail=str(e))

def create_user(user: UserCreate, hashed_password: str, db: Session):
    # Create a new user object with the provided details
    new_user = User(
        first_name=user.firstname,
        last_name=user.lastname,
        email=user.email,
        username=user.username,
        password=hashed_password
    )

    # Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/register", tags=["Register"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists in the database
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password before storing in the database
    hashed_password = get_password_hash(user.password)

    # Create the user in the database
    created_user = create_user(user, hashed_password, db)

    return {"message": "User registered successfully"}

@router.post("/login", tags=["Login"])
def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if user and user.login_attempts_left <= 0:
        createLoginHistory(False, user.id, db, request, "Too many login attempts user is lock")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Too many login attempts user is lock")
    # print("user => ", user.password)
    # Verify the password
    if not user or not verify_password(form_data.password, user.password):
        if user:
            user.login_attempts_left -= 1
            createLoginHistory(False, user.id, db, request)
            
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        
    if user.login_attempts_left <= 0:
        createLoginHistory(False, user.id, db, request, "Too many login attempts profile is lock")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Too many login attempts profile is lock")
    # Generate the access token
    user.login_count += 1
    user.login_attempts_left = 5
    db.commit()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    createLoginHistory(True, user.id, db, request)

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/current_user", tags=["Current User"])
def current_user(user: User = Depends(get_user_from_token)):
    user.password = 'Password Cant be shared'
    return user

@router.get("login-history", tags=["Login History"])
async def login_history(db: Session = Depends(get_db), current_user: User = Depends(get_user_from_token)):
    return db.query(LoginHistory).filter(LoginHistory.user_id == current_user.id).limit(10).all()




