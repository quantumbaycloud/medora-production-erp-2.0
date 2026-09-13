from sqlalchemy.orm import Session

from app.user.models import User


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone: str) -> User | None:
    return db.query(User).filter(User.phone == phone).first()


def update_user(db: Session, user: User, name: str | None) -> User:
    if name is not None:
        user.name = name
    db.commit()
    db.refresh(user)
    return user
