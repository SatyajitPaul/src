from fastapi import FastAPI

app = FastAPI(title='PreRevise', version='0.1.0')


@app.get("/", tags= ['Home'])
async def root():
    return {"message": "Hello World"}