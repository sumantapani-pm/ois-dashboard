from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api.routes import anomalies, actions, clients, metrics, debug

app = FastAPI(
    title="OIS — Operational Intelligence System API",
    version="1.0.0",
    description="Action layer for anomaly remediation"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ois-dashboard.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anomalies.router, prefix="/anomalies", tags=["Anomalies"])
app.include_router(actions.router, prefix="/actions", tags=["Actions"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])
app.include_router(debug.router, prefix="/debug", tags=["Debug"])

@app.get("/health")
def health():
    return {"status": "OIS operational"}
