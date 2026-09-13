import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import api from "../services/api";

export default function ProtectedRoute({ requireLicense = true }) {
  const location = useLocation();
  const [state, setState] = useState("checking");
  useEffect(() => {
    let active = true;
    const token = localStorage.getItem("accessToken");
    if (!token) { setState("unauthenticated"); return () => { active = false; }; }
    const verify = async () => {
      try {
        const me = await api.get("/auth/me");
        if (!active) return;
        const user = me.data?.user || me.data;
        if (user) localStorage.setItem("user", JSON.stringify(user));
        if (!requireLicense) { setState("authenticated"); return; }
        await api.get("/api/licensing/status");
        if (active) setState("authenticated");
      } catch (error) {
        if (!active) return;
        const code = error?.response?.status;
        if (code === 401) {
          localStorage.removeItem("accessToken"); localStorage.removeItem("refreshToken"); localStorage.removeItem("user");
          setState("unauthenticated");
        } else if (code === 403) setState("license");
        else setState("unavailable");
      }
    };
    verify();
    return () => { active = false; };
  }, [location.pathname, requireLicense]);
  if (state === "checking") return <div className="min-h-screen flex items-center justify-center">Checking MEDORAX ERP access…</div>;
  if (state === "unauthenticated") return <Navigate to="/login" replace state={{ from: location }} />;
  if (state === "license") return <Navigate to="/license" replace state={{ from: location }} />;
  if (state === "unavailable") return <div className="min-h-screen flex items-center justify-center bg-background p-6"><div className="max-w-md rounded-xl border border-outline-variant bg-surface-container-lowest p-6 text-center"><h1 className="text-lg font-bold text-on-background">ERP access verification unavailable</h1><p className="mt-2 text-sm text-on-surface-variant">MEDORAX could not verify the session or license. Access is blocked until the service is available.</p><button onClick={() => window.location.reload()} className="mt-5 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-on-primary">Retry</button></div></div>;
  return <Outlet />;
}
