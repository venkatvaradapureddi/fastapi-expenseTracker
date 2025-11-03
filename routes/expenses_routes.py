from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import  OAuth2PasswordBearer
import schemas,db,auth
from models import Expense,User
from jose import jwt, JWTError

router = APIRouter(tags=["expenses"])
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(db.get_db)):
    try:
        payload = jwt.decode(token,auth.SECRET_KEY,algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_method=400,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user 

@router.get("/expenses",response_model=list[schemas.ExpenseOut])
def get_expenses(current_user:User = Depends(get_current_user),db:Session=Depends(db.get_db)):
    expense = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expense   

@router.post("/expense",response_model = schemas.ExpenseOut)
def post_expense(expense:schemas.ExpenseCreate,db:Session = Depends(db.get_db),current_user: User = Depends(get_current_user)):
    db_expense = Expense(**expense.model_dump(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

