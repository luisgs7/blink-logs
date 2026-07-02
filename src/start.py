from fastapi import FastAPI

app = FastAPI(title="BlinkLogs")


@app.get("/ping")
def ping():
    return {"status": "online ;)"} 
 