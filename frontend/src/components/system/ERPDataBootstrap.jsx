import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { loadERPData, clearERPData } from "../../services/erpDataBootstrap";

export default function ERPDataBootstrap({ children }) {
  const authenticated = useSelector((state) => state.auth?.isAuthenticated);
  const [state, setState] = useState("idle");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    if (!authenticated) {
      clearERPData();
      setState("idle");
      return () => { active = false; };
    }
    setState("loading");
    setError("");
    loadERPData()
      .then(() => active && setState("ready"))
      .catch((err) => {
        if (!active) return;
        setError(err?.response?.data?.detail || err?.message || "Unable to load ERP workspace data.");
        setState("error");
      });
    return () => { active = false; };
  }, [authenticated]);

  if (authenticated && state === "loading") {
    return <div className="min-h-screen flex items-center justify-center bg-background text-on-background">Loading MEDORAX workspace…</div>;
  }
  if (authenticated && state === "error") {
    return <div className="min-h-screen flex items-center justify-center bg-background p-6"><div className="max-w-lg rounded-xl border border-outline-variant bg-surface-container-lowest p-6"><h1 className="text-lg font-bold text-on-background">Workspace unavailable</h1><p className="mt-2 text-sm text-on-surface-variant">{error}</p><button className="mt-4 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-on-primary" onClick={() => window.location.reload()}>Retry</button></div></div>;
  }
  return children;
}
