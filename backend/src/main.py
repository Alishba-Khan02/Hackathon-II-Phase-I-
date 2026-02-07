from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .models import User, Task
from .database import create_db_and_tables, get_session
from .services.auth import verify_password, get_password_hash, create_access_token, get_current_user
from .api import tasks  # Tasks router

app = FastAPI()

# ⚡ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include tasks router
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ---------------------------
# Auth & Users Endpoints
# ---------------------------

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # ✅ Check if username already exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Hash the plain password
    hashed_password = get_password_hash(user.password_hash)
    user.password_hash = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
