from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

from agent.controller import RPABotFailureAgent

app = FastAPI(
    title="Agentic RPA Failure Analyzer",
    description="Autonomous analysis of UiPath bot failures",
    version="1.0.0"
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_logs(file: UploadFile = File(...)):
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run agent
    agent = RPABotFailureAgent(log_path=file_path)
    result = agent.run()

    return {
        "file": file.filename,
        "analysis_result": result
    }
