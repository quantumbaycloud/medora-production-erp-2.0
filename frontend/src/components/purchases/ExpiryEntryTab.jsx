import { Package, AlertTriangle, X } from "lucide-react";
import { Th, Td, StatCard } from "./Shared";

export default function ExpiryEntryTab({ receivedItems, itemBatches, updateItemData, calculateShelfLife, expiryStats }) {
  const hasAlerts = expiryStats.expired > 0 || expiryStats.near > 0;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard label="Total Batches" value={expiryStats.total} icon={Package} />
        <StatCard label="Near Expiry" value={expiryStats.near} icon={AlertTriangle} iconColor="text-[#ba1a1a]" subtext="Requires attention" />
        <StatCard label="Expired" value={expiryStats.expired} icon={X} iconColor="text-[#ba1a1a]" subtext="Needs immediate action" />
      </div>

      <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#eff4ff] font-label-md text-[#121c2a] border-b border-[#c2c6d3] uppercase tracking-wider text-[11px]">
                <Th>Item Name</Th>
                <Th>Batch No.</Th>
                <Th className="w-48">Expiry Date</Th>
                <Th className="w-40">Shelf Life</Th>
                <Th className="text-center">Status</Th>
              </tr>
            </thead>
            <tbody className="font-body-md text-[#424751] divide-y divide-[#c2c6d3]">
              {receivedItems.map((item) => {
                const batches = itemBatches[item.id] || [{ batchNo: item.batch, qty: item.received }];
                return batches.map((batch, idx) => {
                  const life = calculateShelfLife(item.expiry);
                  const rowBg =
                    life.status === "EXPIRED"
                      ? "bg-[#ffdad6] hover:bg-[#ffdad6]"
                      : life.status === "NEAR EXPIRY"
                      ? "bg-[#ffdad6] hover:bg-[#ffdad6]"
                      : "hover:bg-[#eff4ff]";
                  return (
                    <tr key={`${item.id}-${idx}`} className={`transition-colors border-b border-[#c2c6d3] ${rowBg}`}>
                      <Td className="font-medium text-[#121c2a]">{item.name}</Td>
                      <Td className="text-[#424751] font-mono text-[13px]">{batch.batchNo || "-"}</Td>
                      <Td>
                        <input
                          type="month"
                          value={item.expiry}
                          onChange={(e) => updateItemData(item.id, "expiry", e.target.value)}
                          className="bg-transparent border border-[#c2c6d3] rounded p-1 outline-none focus:border-[#004287] focus:ring-2 focus:ring-[#d6e3ff] text-[#121c2a]"
                        />
                      </Td>
                      <Td>
                        <span className="text-[#424751] font-medium">{life.months} months</span>
                      </Td>
                      <Td className="text-center">
                        <span className={`inline-flex px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${life.badgeClass}`}>
                          {life.status}
                        </span>
                      </Td>
                    </tr>
                  );
                });
              })}
            </tbody>
          </table>
        </div>
      </div>

      {hasAlerts && (
        <div className="p-4 rounded bg-[#ffdad6] border border-[#ba1a1a] flex items-center gap-3 text-[#ba1a1a]">
          <AlertTriangle size={18} className="flex-shrink-0" />
          <p className="font-body-md font-medium">Some items have expired or are nearing expiry. Please verify before confirming receipt.</p>
        </div>
      )}
    </div>
  );
}
