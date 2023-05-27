from sqlalchemy import ForeignKey
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


from database import Base
#This will create a table that will store follower details
class Follow(Base):
    __tablename__ = "follows"

    id = mapped_column(Integer, primary_key=True, index=True)
    start_following = mapped_column(DateTime, default=datetime.now())
    follower_id = mapped_column(Integer, ForeignKey("users.id"))
    following_id = mapped_column(Integer, ForeignKey("users.id"))

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
