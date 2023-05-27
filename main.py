from fastapi import FastAPI, Depends
#Local Import Files
from database import engine
import models
from routers import auth, post, follow
from doc.basic import tags
from routers.auth import get_user_from_token
# from routers.auth import has_access
#from emailUtil import send_confirmation_email

PROTECTED = [Depends(get_user_from_token)]

app = FastAPI(title='PreRevise', version='0.1.0', openapi_tags=tags)
models.Base.metadata.create_all(engine)
app.include_router(auth.router)
app.include_router(post.router, dependencies=PROTECTED)
app.include_router(follow.router)


@app.get("/", tags= ['Home'])
async def root():
    """This is the Root of the Application

    Returns:
        None
    """
    return {"message": "Welcome to the Pre-Revise"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)