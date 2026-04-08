from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus
from app.utils.security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        phone: str = payload.get("sub")
        if not phone:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise credentials_exception
    if user.status == UserStatus.blocked.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь заблокирован",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: UserRole):
    allowed = {
        role if isinstance(role, UserRole) else UserRole(role)
        for role in allowed_roles
    }

    def _role_checker(current_user: User = Depends(get_current_user)) -> User:
        current_role = current_user.role if isinstance(current_user.role, UserRole) else UserRole(current_user.role)
        if current_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )
        return current_user

    return _role_checker


def admin_required(current_user: User = Depends(require_roles(UserRole.admin))):
    return current_user
