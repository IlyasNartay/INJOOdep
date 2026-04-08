import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_current_user
from app.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.constants.user_roles import USER_ROLE_LABELS
from app.schemas.user import AuthMetaResponse, LoginRequest, RoleOption, StatusOption, Token, UserCreate, UserOut
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter()

# Регулярка для казахстанских номеров
KZ_PHONE_REGEX = re.compile(r"^(?:\+7|8)7\d{9}$")

def validate_kz_phone(phone: str):
    if not KZ_PHONE_REGEX.match(phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный формат казахстанского номера")
    return phone

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()


@router.get("/meta", response_model=AuthMetaResponse)
def auth_meta():
    return AuthMetaResponse(
        roles=[
            RoleOption(key=UserRole.admin, label=USER_ROLE_LABELS[UserRole.admin.value]),
            RoleOption(key=UserRole.staff, label=USER_ROLE_LABELS[UserRole.staff.value]),
            RoleOption(key=UserRole.customer, label=USER_ROLE_LABELS[UserRole.customer.value]),
        ],
        statuses=[
            StatusOption(key=UserStatus.active.value, label="Активен"),
            StatusOption(key=UserStatus.blocked.value, label="Заблокирован"),
        ],
        guest_mode="guest",
    )


@router.get("/me", response_model=UserOut)
def auth_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    validate_kz_phone(user_in.phone)

    if get_user_by_phone(db, user_in.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Телефон уже зарегистрирован")

    user = User(
        phone=user_in.phone,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        role=UserRole.customer,
        status=UserStatus.active.value
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.phone})
    return Token(access_token=access_token, token_type="bearer", user_role=user.role, user_status=user.status)


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # validate_kz_phone(phone)

    user = get_user_by_phone(db, login_data.phone)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный номер или пароль")

    if user.status == UserStatus.blocked.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь заблокирован")

    access_token = create_access_token(data={"sub": user.phone})
    return Token(access_token=access_token, token_type="bearer", user_role=user.role, user_status=user.status)
