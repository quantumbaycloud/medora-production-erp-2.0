import { useEffect, useState } from "react";
import { RefreshCw, ShieldCheck } from "lucide-react";
import api, { withPharmacy } from "../../services/api";

const TYPES = [
  ["supplier_category", "Supplier Categories"],
  ["medicine_category", "Medicine Categories"],
  ["payment_term", "Payment Terms"],
  ["customer_type", "Customer Types"],
  ["dosage_form", "Dosage Forms"],
  ["unit", "Units"],
];

export default function MasterData() {
  const [items, setItems] = useState([]);
  const [type, setType] = useState("supplier_category");
  const [loading, setLoading] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncError, setSyncError] = useState("");

  const load = async () => {
    setLoading(true);
    setSyncError("");

    try {
      const params = withPharmacy();

      // Admin is authoritative for pharmacy-specific master data.
      // This is an outbound ERP -> Admin request and does not require an
      // inbound Cloudflare tunnel to the local ERP.
      setSyncing(true);
      await api.post("/admin-sync/catalog", null, { params });
    } catch (error) {
      // Keep the locally cached catalog usable during a temporary Admin outage.
      setSyncError(
        error?.response?.data?.detail ||
          error?.message ||
          "Admin catalog sync unavailable; showing local catalog cache.",
      );
    } finally {
      setSyncing(false);
    }

    try {
      const { data } = await api.get("/catalog", {
        params: { ...withPharmacy(), option_type: type },
      });
      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("[MasterData] catalog load failed", error);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [type]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-on-background">Master Data</h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Pharmacy-specific options are controlled by Medorax Admin and
          synchronized to this licensed ERP.
        </p>
      </div>

      <div className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-5 flex flex-col md:flex-row gap-3 md:items-center">
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="rounded-xl border border-outline-variant p-3 bg-white"
        >
          {TYPES.map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>

        <button
          onClick={load}
          disabled={loading || syncing}
          className="inline-flex items-center gap-2 rounded-xl border border-outline-variant px-4 py-3 text-sm font-semibold disabled:opacity-60"
        >
          <RefreshCw
            size={16}
            className={loading || syncing ? "animate-spin" : ""}
          />
          {syncing ? "Syncing Admin…" : loading ? "Loading…" : "Refresh"}
        </button>

        <span className="ml-auto inline-flex items-center gap-2 text-xs text-on-surface-variant">
          <ShieldCheck size={15} />
          {syncError ? "Admin sync unavailable" : "Admin synchronized"}
        </span>
      </div>

      {syncError && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          {syncError}
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <div
            key={item.id}
            className="rounded-xl border border-outline-variant bg-surface-container-lowest p-4"
          >
            <div className="font-semibold">{item.name}</div>
            <div className="mt-1 text-xs font-mono text-outline">
              {item.code}
            </div>
          </div>
        ))}

        {!loading && !items.length && (
          <div className="col-span-full rounded-xl border border-dashed border-outline-variant p-10 text-center text-sm text-on-surface-variant">
            No options have been configured by Admin yet.
          </div>
        )}
      </div>
    </div>
  );
}
