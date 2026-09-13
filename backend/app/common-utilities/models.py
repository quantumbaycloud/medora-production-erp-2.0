"""
ORM models backing the three log tables:

- ErrorLog:    unhandled exceptions / application errors
- ActivityLog: user / API activity (who did what, when)
- SystemLog:   background jobs, startup/shutdown, infra-level events

Each table is intentionally simple and indexed on the fields you'd filter on
most often (timestamp, level/severity, source).
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from database import Base


class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    level = Column(String(20), default="ERROR", index=True)   # ERROR, CRITICAL
    source = Column(String(120), index=True)                  # module / service name
    message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    request_path = Column(String(255), nullable=True)
    user_id = Column(String(80), nullable=True)

    __table_args__ = (Index("ix_error_logs_ts_level", "timestamp", "level"),)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = Column(String(80), index=True, nullable=True)
    action = Column(String(120), index=True)                  # e.g. "LOGIN", "UPDATE_PROFILE"
    resource = Column(String(120), nullable=True)              # e.g. "order:1234"
    ip_address = Column(String(45), nullable=True)
    status = Column(String(20), default="SUCCESS")             # SUCCESS, FAILURE
    details = Column(Text, nullable=True)

    __table_args__ = (Index("ix_activity_logs_ts_user", "timestamp", "user_id"),)


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    level = Column(String(20), default="INFO", index=True)    # DEBUG, INFO, WARNING, ERROR
    component = Column(String(120), index=True)                # e.g. "scheduler", "db-pool"
    message = Column(Text, nullable=False)

    __table_args__ = (Index("ix_system_logs_ts_level", "timestamp", "level"),)
