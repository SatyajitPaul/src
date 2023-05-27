from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import mapped_column, Session
from sqlalchemy.orm import relationship, validates
from datetime import datetime
from models.util import PrivacyType


from database import Base


#Create a User Class to store end user information
class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(32), unique=True, index=True, nullable=False)
    email = mapped_column(String(64), unique=True, index=True, nullable=False)
    password = mapped_column(String)
    first_name = mapped_column(String(32))
    last_name = mapped_column(String(32))
    followers_count = mapped_column(Integer, default=0)
    following_count = mapped_column(Integer, default=0)
    post_count = mapped_column(Integer, default=0)
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=datetime.now)
    email_verified = mapped_column(Boolean, default=False)
    email_verified_at = mapped_column(DateTime)
    privacy_type = mapped_column(Enum(PrivacyType), default=PrivacyType.PUBLIC)

    posts = relationship("Post", back_populates="user")

    followers = relationship("Follow", back_populates="following", foreign_keys='[Follow.following_id]')
    following = relationship("Follow", back_populates="follower", foreign_keys='[Follow.follower_id]')

    login_history = relationship("LoginHistory", back_populates="user")
    login_count = mapped_column(Integer, default=0)
    login_attempts_left = mapped_column(Integer, default=5)


##Get User
def get_user(db: Session, user_id: int):
    """_summary_

    Args:
        db (Session): _description_
        user_id (int): _description_

    Returns:
        _type_: _description_
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


##Get User By Email
def get_user_by_email(db: Session, email: str):
    """_summary_

    Args:
        db (Session): _description_
        email (str): _description_

    Returns:
        _type_: _description_
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()