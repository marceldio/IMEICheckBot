import os
import sys

from fastapi import FastAPI

from app.api import router

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

app = FastAPI(title="IMEICheckBot API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
