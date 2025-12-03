from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import User, Progress, Program
from .schemas import UserCreate, UserLogin, Attempt, ProgramEntry

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 允许前端访问 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== 注册 ==========
@app.post("/api/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return {"success": False, "error": "Username already exists"}

    hashed = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed)
    db.add(new_user)
    db.commit()
    return {"success": True}


# ========== 登录 ==========
@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        return {"success": False, "error": "User not found"}

    if not pwd_context.verify(user.password, db_user.password_hash):
        return {"success": False, "error": "Incorrect password"}

    return {"success": True, "role": db_user.role, "user_id": db_user.id}


# ========== 保存训练记录 ==========
@app.post("/api/saveAttempt")
def save_attempt(attempt: Attempt, user_id: int, db: Session = Depends(get_db)):
    entry = Progress(
        user_id=user_id,
        drill_id=attempt.drill_id,
        drill_title=attempt.drill_title,
        reps=attempt.reps,
        seconds=attempt.seconds,
        rate=attempt.rate,
        date=attempt.date
    )
    db.add(entry)
    db.commit()
    return {"success": True}


# ========== 获取历史记录 ==========
@app.get("/api/history")
def get_history(user_id: int, db: Session = Depends(get_db)):
    entries = db.query(Progress).filter(Progress.user_id == user_id).all()
    return entries


# ========== 保存 30 天计划 ==========
@app.post("/api/program")
def save_program(program: list[ProgramEntry], user_id: int, db: Session = Depends(get_db)):
    db.query(Program).filter(Program.user_id == user_id).delete()
    db.commit()

    for entry in program:
        db.add(Program(
            user_id=user_id,
            day_number=entry.day_number,
            drill_id=entry.drill_id,
            reps=entry.reps,
            minutes=entry.minutes
        ))
    db.commit()

    return {"success": True}


# ========== 获取 30 天计划 ==========
@app.get("/api/program")
def get_program(user_id: int, db: Session = Depends(get_db)):
    return db.query(Program).filter(Program.user_id == user_id).all()
