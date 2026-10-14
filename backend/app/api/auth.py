from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.schemas import UserCreate, UserResponse, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.database import get_database
from datetime import datetime
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# In-memory user store for demo/standalone running if MongoDB is not present
in_memory_users = {
    "admin@healthcare.ai": {
        "id": "usr_admin_001",
        "email": "admin@healthcare.ai",
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "role": "lead_researcher",
        "created_at": datetime.utcnow()
    }
}

@router.post("/register", response_model=UserResponse)
async def register_user(user_in: UserCreate):
    db_conn = await get_database()
    
    # Check if user exists in MongoDB or fallback
    existing_user = None
    if db_conn is not None:
        try:
            existing_user = await db_conn["users"].find_one({"email": user_in.email})
        except Exception:
            pass

    if existing_user or user_in.email in in_memory_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    hashed_pwd = get_password_hash(user_in.password)
    
    user_dict = {
        "id": user_id,
        "email": user_in.email,
        "username": user_in.username,
        "hashed_password": hashed_pwd,
        "role": user_in.role or "researcher",
        "created_at": datetime.utcnow()
    }

    if db_conn is not None:
        try:
            await db_conn["users"].insert_one(user_dict)
        except Exception:
            in_memory_users[user_in.email] = user_dict
    else:
        in_memory_users[user_in.email] = user_dict

    return UserResponse(
        id=user_id,
        email=user_in.email,
        username=user_in.username,
        role=user_dict["role"],
        created_at=user_dict["created_at"]
    )

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = None
    db_conn = await get_database()
    
    if db_conn is not None:
        try:
            user_record = await db_conn["users"].find_one({"email": form_data.username})
        except Exception:
            pass
            
    if not user_record and form_data.username in in_memory_users:
        user_record = in_memory_users[form_data.username]

    if not user_record or not verify_password(form_data.password, user_record["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user_record["email"])
    
    user_resp = UserResponse(
        id=user_record.get("id", "usr_demo"),
        email=user_record["email"],
        username=user_record["username"],
        role=user_record.get("role", "researcher"),
        created_at=user_record.get("created_at", datetime.utcnow())
    )

    return Token(access_token=access_token, token_type="bearer", user=user_resp)
