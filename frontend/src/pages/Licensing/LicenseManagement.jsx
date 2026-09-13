import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import licenseService from "../../services/licensing/licenseService";

const LicenseManagement = () => {
  const token = useSelector((state) => state.auth?.token) || localStorage.getItem("accessToken");
  const user = useSelector((state) => state.auth?.user) || (() => { try { return JSON.parse(localStorage.getItem("user") || "null"); } catch { return null; } })();
  const tenantId = user?.pharmacy_id || user?.pharmacyId || "";
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const load = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const { data } = await licenseService.status(token, tenantId);
      setStatus(data); setMessage("");
    } catch (e) { setMessage(e.response?.data?.detail || "Unable to read license status"); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, [token, tenantId]);


  const active = status?.status === "active";
  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div><h1 className="text-2xl font-bold">MEDORAX ERP License</h1><p className="text-sm opacity-70">Secure license activation and device management.</p></div>
      {active ? (
        <div className="rounded-2xl border p-6 space-y-5">
          <div className="flex items-center justify-between gap-4">
            <div><div className="text-xs opacity-60">License status</div><div className="text-xl font-semibold capitalize">{status.status}</div></div>
            <div className="rounded-full px-4 py-2 border text-sm">Automatically verified</div>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div><div className="text-xs opacity-60">License ID</div><div className="font-mono text-sm break-all">{status.license_id || "—"}</div></div>
            <div><div className="text-xs opacity-60">Plan</div><div>{status.plan || "—"}</div></div>
            <div><div className="text-xs opacity-60">Expires</div><div>{status.expires_at ? new Date(status.expires_at).toLocaleString() : "—"}</div></div>
            <div><div className="text-xs opacity-60">Device limit</div><div>{status.max_devices ?? "—"}</div></div>
          </div>
          <div><div className="text-xs opacity-60">Enabled modules</div><div className="mt-1">{status.modules?.length ? status.modules.join(", ") : "—"}</div></div>
          <p className="text-sm opacity-70">Licensing is provisioned and controlled by MEDORAX onboarding. No license key or manual activation is required in the ERP.</p>
        </div>
      ) : (
        <div className="rounded-2xl border p-6">
          <h2 className="text-lg font-semibold">ERP license unavailable</h2>
          <p className="mt-2 text-sm opacity-70">This account has no active onboarding-provisioned license on this ERP tenant. Contact MEDORAX support or the account administrator.</p>
        </div>
      )}
      <button disabled={loading} onClick={load} className="rounded-xl border px-5 py-3 disabled:opacity-50">Refresh status</button>
      {message && <div className="rounded-xl border p-4 text-sm">{message}</div>}
    </div>
  );
};
export default LicenseManagement;
