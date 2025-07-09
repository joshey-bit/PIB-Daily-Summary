from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from backend.run_pipeline import run_pipeline
import threading
import time
from typing import List



app = FastAPI()

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected WebSocket clients
websocket_clients: List[WebSocket] = []

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

@app.get("/summaries/{date}")
def get_summaries(date: str):
    """Return summaries for a given date (YYYY-MM-DD)."""
    file_path = os.path.join(DATA_DIR, f"{date}.json")
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "No data for this date."})
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return data


@app.post("/run-pipeline")
def run_pipeline_now():
    """Manually trigger the pipeline and notify clients."""
    run_pipeline()
    # Notify all connected websocket clients
    for ws in websocket_clients:
        try:
            ws.send_text("update")
        except Exception:
            pass
    return {"status": "Pipeline run complete."}

# WebSocket endpoint for live updates
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        websocket_clients.remove(websocket)

# --- Scheduler for daily run at 9:00 PM ---
def schedule_daily_pipeline():
    while True:
        now = datetime.now()
        # Schedule for 21:00 (9:00 PM)
        run_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
        if now > run_time:
            run_time = run_time.replace(day=now.day + 1)
        wait_seconds = (run_time - now).total_seconds()
        time.sleep(wait_seconds)
        try:
            run_pipeline()
            # Notify all connected websocket clients
            for ws in websocket_clients:
                try:
                    ws.send_text("update")
                except Exception:
                    pass
        except Exception as e:
            print(f"Scheduled pipeline error: {e}")

@app.on_event("startup")
def start_scheduler():
    t = threading.Thread(target=schedule_daily_pipeline, daemon=True)
    t.start()

# To run: uvicorn api_server:app --host 0.0.0.0 --port 8000
