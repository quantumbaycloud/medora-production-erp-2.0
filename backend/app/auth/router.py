"""HTTP API for MEDORAX ERP authentication and session management."""
import secrets
import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session as DbSession

from app.auth import service
from app.auth.models import LoginHistory, Session as AuthSession
from app.auth.schemas import DeviceRead, DeviceUpdate, ForgotPasswordRequest, LoginRequest, RefreshRequest, RegisterRequest, ResendVerificationRequest, ResetPasswordRequest, SessionRead, TokenResponse, VerifyEmailRequest
from app.core.config import settings
from app.db.base import get_db
from app.services.email_service import EmailSendError, send_password_reset_email, send_verification_email
from app.shared.deps import get_current_user
from app.shared.rate_limit import limiter
from app.user.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

def _ip(request: Request): return request.client.host if request.client else None

def _user(user: User, db: DbSession | None = None):
    pharmacies = getattr(user, "pharmacies", None) or []
    pharmacy_id = str(pharmacies[0].id) if pharmacies else None
    role = None
    role_id = None
    if db is not None:
        from app.staff.models import StaffMember
        staff = db.query(StaffMember).filter(StaffMember.user_id == user.id).order_by(StaffMember.created_at.asc()).first()
        if staff and staff.role:
            role = staff.role.name
            role_id = staff.role.id
            pharmacy_id = staff.pharmacy_id
    return {"id": str(user.id), "username": user.username, "name": user.name, "email": user.email, "phone": user.phone, "pharmacy_id": pharmacy_id, "role": role, "role_id": role_id, "email_verified": bool(user.email_verified), "phone_verified": bool(user.phone_verified), "is_active": bool(user.is_active)}

def _email_task(to: str, token: str, kind: str):
    try:
        (send_verification_email if kind == "verification" else send_password_reset_email)(to, token)
    except EmailSendError:
        pass

@router.post("/register", status_code=201)
@limiter.limit(settings.rate_limit_register)
def register(request: Request, payload: RegisterRequest, background_tasks: BackgroundTasks, db: DbSession = Depends(get_db)):
    user, token = service.register_user(db, payload.name, str(payload.email) if payload.email else None, payload.phone, payload.password)
    if token and user.email: background_tasks.add_task(_email_task, user.email, token, "verification")
    return {"user": _user(user, db), "message": "Registration successful"}

@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: DbSession = Depends(get_db)):
    service.verify_email_token(db, payload.token); return {"status":"verified"}

@router.post("/resend-verification")
@limiter.limit(settings.rate_limit_resend_verification)
def resend_verification(request: Request, payload: ResendVerificationRequest, background_tasks: BackgroundTasks, db: DbSession = Depends(get_db)):
    token = service.resend_verification_email(db, str(payload.email))
    if token: background_tasks.add_task(_email_task, str(payload.email), token, "verification")
    return {"message":"If the account requires verification, a new email has been sent."}

@router.post("/forgot-password")
@limiter.limit(settings.rate_limit_forgot_password)
def forgot_password(request: Request, payload: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: DbSession = Depends(get_db)):
    token = service.forgot_password(db, payload.identifier)
    if token:
        user = service._get_user_by_identifier(db, payload.identifier)
        if user and user.email: background_tasks.add_task(_email_task, user.email, token, "reset")
    return {"message":"If the account exists, password reset instructions have been sent."}

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: DbSession = Depends(get_db)):
    service.reset_password(db, payload.token, payload.password); return {"message":"Password reset successful. Please log in again."}

@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.rate_limit_login)
def login(request: Request, payload: LoginRequest, db: DbSession = Depends(get_db)):
    access, refresh, device = service.authenticate(db, payload.identifier, payload.password, str(payload.device_identifier) if payload.device_identifier else None, payload.device_name, payload.platform, payload.app_version, payload.push_token, _ip(request), request.headers.get("user-agent"))
    user = service._get_user_by_identifier(db, payload.identifier)
    return TokenResponse(access_token=access, refresh_token=refresh, device_identifier=device, user=_user(user, db) if user else None)

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit(settings.rate_limit_refresh)
def refresh(request: Request, payload: RefreshRequest, db: DbSession = Depends(get_db)):
    access, refresh_token = service.refresh_access_token(db, payload.refresh_token)
    try: decoded = jwt.decode(payload.refresh_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError: decoded = {}
    row = db.query(AuthSession).filter(AuthSession.id == decoded.get("sid")).first() if decoded.get("sid") else None
    user = db.query(User).filter(User.id == decoded.get("sub")).first() if decoded.get("sub") else None
    return TokenResponse(access_token=access, refresh_token=refresh_token, device_identifier=row.device.device_identifier if row and row.device else None, user=_user(user, db) if user else None)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    sid = getattr(current_user, "_current_session_id", None)
    if sid: service.logout(db, sid)
    return {"message":"Logged out successfully"}

@router.post("/logout-all")
def logout_all(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    service.logout_all(db, str(current_user.id), getattr(current_user, "_current_session_id", None)); return {"message":"All other sessions revoked"}

@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)): return {"user": _user(current_user, db)}


@router.get("/login-history")
def login_history(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    rows = (db.query(LoginHistory).filter(LoginHistory.user_id == current_user.id).order_by(LoginHistory.created_at.desc()).limit(200).all())
    return [{"id": row.id, "success": bool(row.success), "ip_address": row.ip_address, "user_agent": row.user_agent, "created_at": row.created_at, "device_id": row.device_id} for row in rows]

@router.get("/sessions", response_model=list[SessionRead])
def sessions(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    current = str(getattr(current_user, "_current_session_id", "")); rows=[]
    for row in service.get_user_sessions(db, str(current_user.id)):
        item = SessionRead.model_validate(row); item.is_current = str(row.id) == current; rows.append(item)
    return rows

@router.delete("/sessions/{session_id}")
def revoke_session(session_id: str, current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    service.revoke_session(db, str(current_user.id), session_id); return {"message":"Session revoked"}

@router.get("/devices", response_model=list[DeviceRead])
def devices(current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)): return service.get_user_devices(db, str(current_user.id))

@router.patch("/devices/{device_id}", response_model=DeviceRead)
def update_device(device_id: str, payload: DeviceUpdate, current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    return service.update_device(db, str(current_user.id), device_id, payload.friendly_name, payload.trusted)

@router.post("/devices/{device_id}/deactivate")
def deactivate_device(device_id: str, current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    service.deactivate_device(db, str(current_user.id), device_id); return {"message":"Device deactivated"}

internal_router = APIRouter(prefix="/internal", tags=["internal"])
def require_internal_key(x_internal_key: str | None = Header(default=None)):
    expected = settings.internal_api_key
    if not expected: raise HTTPException(503, "Internal API key is not configured")
    if not x_internal_key or not secrets.compare_digest(x_internal_key, expected): raise HTTPException(401, "Invalid internal API key")

@internal_router.post("/cleanup", dependencies=[Depends(require_internal_key)])
def cleanup(db: DbSession = Depends(get_db)):
    from app.services.cleanup import run_all_cleanup
    return run_all_cleanup(db)
