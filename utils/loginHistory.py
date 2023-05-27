from models import LoginHistory
from sqlalchemy.orm import Session
from fastapi import Request
from models import LoginHistory
from datetime import datetime

def createLoginHistory(success: bool, user_id: int ,db: Session, request: Request, msg: str = "No Error"):
    print(request.headers)
    login_history = LoginHistory(
        user_id=user_id,
        timestamp=datetime.now(),
        success=success,
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        device_name=request.headers.get("Device-Name"),
        location=request.headers.get("Location"),
        message = msg
    )

    db.add(login_history)
    db.commit()
    db.refresh(login_history)
    
    return login_history
