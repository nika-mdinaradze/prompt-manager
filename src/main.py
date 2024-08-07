from fastapi import FastAPI

app = FastAPI(
    title="prompt management API", description="Technical Assignment", version="0.0.0"
)


@app.get("/")
def root():
    return {"message": "root url"}
