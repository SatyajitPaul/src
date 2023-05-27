from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from database import Base

#This class will store user login history
class LoginHistory(Base):
    __tablename__ = 'login_history'
    id = mapped_column(Integer, primary_key=True, index=True)

    user_id = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="login_history")

    timestamp = mapped_column(DateTime)
    success = mapped_column(Boolean)
    ip_address = mapped_column(String)
    user_agent = mapped_column(String)
    device_name = mapped_column(String)
    location = mapped_column(String)

    message = mapped_column(String(100), default="No Error")