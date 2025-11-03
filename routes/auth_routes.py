from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import schemas,db,auth
from models import User

router = APIRouter(tags=["auth"])

@router.post("/signup",response_model=schemas.UserOut)
def SignUp(user:schemas.UserCreate,db:Session=Depends(db.get_db)):
    exist_user=db.query(User).filter(user.username == User.username).first()
    exist_email=db.query(User).filter(user.email == User.email).first()
    if exist_user:
        raise HTTPException(Status_code=400,detail="username already exists")
    if exist_email:
        raise HTTPException(Status_code=40,detail="email already exists")
    hashed_password = auth.hash_password(user.password)
    new_user = User(username=user.username,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=schemas.Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(db.get_db)):
    exist_user=db.query(User).filter(User.username == form_data.username).first()
    if not exist_user or not auth.verify_password(form_data.password,exist_user.password):
        raise HTTPException(status_code=400,detail="username or password incorrect")
    token=auth.create_access_token({"sub":exist_user.username})
    return {"access_token":token,"token_type":"bearer"}

