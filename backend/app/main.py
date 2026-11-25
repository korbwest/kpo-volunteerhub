from fastapi import FastAPI

app = FastAPI(title="VolunteerHub")


@app.get("/health")
def health():
    return {"status": "ok"}
