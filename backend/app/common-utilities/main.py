"""
Common Utilities service.

Exposes:
    GET  /health                  -> Health Check
    POST /logs/errors             -> record an error
    GET  /logs/errors             -> query error logs
    POST /logs/activity           -> record an activity event (usually automatic, see middleware)
    GET  /logs/activity           -> query activity logs
    POST /logs/system             -> record a system event
    GET  /logs/system             -> query system logs

Run with:  uvicorn app.main:app --reload
Docs at:   http://localhost:8000/docs
"""
import logging
import traceback
from typing import Optional

from fastapi import FastAPI, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db
from health import run_health_check
from middleware import ActivityLoggingMiddleware
from logging_config import error_logger, activity_logger, system_logger, log_with_extra

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Common Utilities", version="1.0.0")
app.add_middleware(ActivityLoggingMiddleware)


# ---------------------------------------------------------------------------
# Global exception handler -> every unhandled error is captured automatically
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    db = next(get_db())
    tb = traceback.format_exc()
    log_with_extra(error_logger, logging.ERROR, str(exc), path=str(request.url.path))
    try:
        db.add(models.ErrorLog(
            level="CRITICAL",
            source="unhandled_exception",
            message=str(exc),
            stack_trace=tb,
            request_path=str(request.url.path),
        ))
        db.commit()
    finally:
        db.close()
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/health", response_model=schemas.HealthCheckOut, tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    return run_health_check(db)


# ---------------------------------------------------------------------------
# Error Logs
# ---------------------------------------------------------------------------
@app.post("/logs/errors", response_model=schemas.ErrorLogOut, tags=["Error Logs"])
def create_error_log(payload: schemas.ErrorLogCreate, db: Session = Depends(get_db)):
    log_with_extra(error_logger, logging.ERROR, payload.message, source=payload.source)
    entry = models.ErrorLog(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/logs/errors", response_model=list[schemas.ErrorLogOut], tags=["Error Logs"])
def list_error_logs(
    level: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(models.ErrorLog)
    if level:
        q = q.filter(models.ErrorLog.level == level)
    if source:
        q = q.filter(models.ErrorLog.source == source)
    return q.order_by(models.ErrorLog.timestamp.desc()).limit(limit).all()


# ---------------------------------------------------------------------------
# Activity Logs
# ---------------------------------------------------------------------------
@app.post("/logs/activity", response_model=schemas.ActivityLogOut, tags=["Activity Logs"])
def create_activity_log(payload: schemas.ActivityLogCreate, db: Session = Depends(get_db)):
    log_with_extra(activity_logger, logging.INFO, payload.action, user_id=payload.user_id)
    entry = models.ActivityLog(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/logs/activity", response_model=list[schemas.ActivityLogOut], tags=["Activity Logs"])
def list_activity_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(models.ActivityLog)
    if user_id:
        q = q.filter(models.ActivityLog.user_id == user_id)
    if action:
        q = q.filter(models.ActivityLog.action == action)
    return q.order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()


# ---------------------------------------------------------------------------
# System Logs
# ---------------------------------------------------------------------------
@app.post("/logs/system", response_model=schemas.SystemLogOut, tags=["System Logs"])
def create_system_log(payload: schemas.SystemLogCreate, db: Session = Depends(get_db)):
    log_with_extra(system_logger, logging.INFO, payload.message, component=payload.component)
    entry = models.SystemLog(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/logs/system", response_model=list[schemas.SystemLogOut], tags=["System Logs"])
def list_system_logs(
    level: Optional[str] = None,
    component: Optional[str] = None,
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(models.SystemLog)
    if level:
        q = q.filter(models.SystemLog.level == level)
    if component:
        q = q.filter(models.SystemLog.component == component)
    return q.order_by(models.SystemLog.timestamp.desc()).limit(limit).all()
