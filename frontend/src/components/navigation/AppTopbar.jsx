import { useEffect, useRef, useState } from "react";
import { Bell, ChevronDown, LogOut, Menu, ShieldCheck, UserCircle } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../../services/api";
import authService from "../../store/authService";

const initials = (name = "") => name.trim().split(/\s+/).slice(0, 2).map((x) => x[0]).join("").toUpperCase() || "U";

export default function AppTopbar({ onMenuClick }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("user") || "null"); } catch { return null; }
  });
  const [license, setLicense] = useState(null);
  const [notificationCount, setNotificationCount] = useState(0);
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    let active = true;
    Promise.all([
      api.get("/auth/me"),
      api.get("/api/licensing/status"),
      api.get("/notifications", { params: { limit: 100 } }),
    ]).then(([me, lic, notifications]) => {
      if (!active) return;
      const nextUser = me.data?.user || me.data;
      if (nextUser) {
        setUser(nextUser);
        localStorage.setItem("user", JSON.stringify(nextUser));
      }
      if (lic.data) setLicense(lic.data);
      const rows = Array.isArray(notifications.data) ? notifications.data : [];
      setNotificationCount(rows.filter((item) => !item.is_read && !item.read).length);
    }).catch(() => {});
    return () => { active = false; };
  }, []);

  useEffect(() => {
    const close = (event) => { if (!ref.current?.contains(event.target)) setOpen(false); };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  const logout = async () => {
    try { await authService.logout(); } catch { /* local cleanup still happens */ }
    setOpen(false);
    navigate("/login", { replace: true });
  };

  const name = user?.name || user?.username || "User";
  const role = user?.role || user?.role_name || "Account";

  return (
    <header className="fixed left-0 right-0 top-0 z-30 flex h-16 items-center justify-between border-b border-outline-variant bg-surface-container-lowest px-4 shadow-sm md:left-[260px] md:px-8">
      <div className="flex items-center gap-3">
        <button type="button" aria-label="Open navigation" onClick={onMenuClick} className="rounded-lg p-2 text-on-surface-variant transition-colors hover:bg-surface-container md:hidden"><Menu size={22} /></button>
        <div><p className="text-base font-bold tracking-tight text-primary">MEDORAX</p><p className="hidden text-xs text-on-surface-variant sm:block">Pharmacy management workspace</p></div>
      </div>
      <div className="flex items-center gap-3">
        <Link to="/" aria-label="Notifications" className="relative rounded-full p-2 text-on-surface-variant transition-colors hover:bg-surface-container">
          <Bell size={20} />
          {notificationCount > 0 && <span className="absolute right-1 top-1 min-w-4 rounded-full bg-error px-1 text-center text-[9px] font-bold leading-4 text-white">{notificationCount > 99 ? "99+" : notificationCount}</span>}
        </Link>
        <div className="h-8 w-px bg-outline-variant" />
        <div className="relative" ref={ref}>
          <button type="button" onClick={() => setOpen((v) => !v)} aria-expanded={open} className="flex items-center gap-2 rounded-xl px-2 py-1 transition-colors hover:bg-surface-container-low">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-bold text-on-primary">{initials(name)}</span>
            <span className="hidden text-left lg:block"><span className="block max-w-40 truncate text-sm font-semibold text-on-background">{name}</span><span className="block max-w-40 truncate text-xs text-on-surface-variant">{role}</span></span>
            <ChevronDown size={16} className="text-outline" />
          </button>
          {open && (
            <div className="absolute right-0 top-12 w-72 overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-2xl">
              <div className="border-b border-outline-variant p-4">
                <div className="flex items-center gap-3"><div className="flex h-11 w-11 items-center justify-center rounded-full bg-primary text-sm font-bold text-on-primary">{initials(name)}</div><div className="min-w-0"><p className="truncate font-semibold text-on-background">{name}</p><p className="truncate text-xs text-on-surface-variant">{user?.email || user?.phone || user?.username || ""}</p></div></div>
                {license && <div className="mt-3 flex items-center gap-2 rounded-lg bg-surface-container-low px-3 py-2 text-xs"><ShieldCheck size={15} className="text-primary" /><span className="font-medium">License: {license.status || "unknown"}</span>{license.expires_at && <span className="ml-auto text-outline">{new Date(license.expires_at).toLocaleDateString("en-IN")}</span>}</div>}
              </div>
              <div className="p-2">
                <Link to="/profile" onClick={() => setOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm hover:bg-surface-container-low"><UserCircle size={18} /> My Profile</Link>
                <Link to="/sessions" onClick={() => setOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm hover:bg-surface-container-low">Active Sessions</Link>
                <Link to="/license" onClick={() => setOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm hover:bg-surface-container-low">License & Devices</Link>
                <button onClick={logout} className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-error hover:bg-error-container"><LogOut size={18} /> Sign out</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
