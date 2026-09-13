import { useMemo } from "react";
import { inventoryData, STAT_LABELS, ROWS_PER_PAGE } from "../../data/reports/data";
import { StatCard, Pagination, Th, Td } from "./Shared";

// Stats Component
export function InventoryStats() {
  const [label1, label2, label3] = STAT_LABELS.inventory;

  const stats = [
    { value: inventoryData.stats.total, icon: "arrow_upward", text: "1.5% vs last month", cls: "text-[#006d40]" },
    { value: inventoryData.stats.expiring, icon: "trending_up", text: "needs attention", cls: "text-[#ba1a1a]" },
    { value: inventoryData.stats.skus, icon: "info", text: "Active SKUs", cls: "text-[#424751]" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard label={label1} value={stats[0].value} trendIcon={stats[0].icon} trendText={stats[0].text} trendClass={stats[0].cls} />
      <StatCard label={label2} value={stats[1].value} trendIcon={stats[1].icon} trendText={stats[1].text} trendClass={stats[1].cls} />
      <StatCard label={label3} value={stats[2].value} trendIcon={stats[2].icon} trendText={stats[2].text} trendClass={stats[2].cls} />
    </div>
  );
}

// Table Component
export function InventoryTable({ inventorySubtype, page, setPage, search }) {
  const filteredRows = useMemo(() => {
    let rows = inventoryData.rows[inventorySubtype] || [];
    if (search) {
      rows = rows.filter((r) => 
        Object.values(r).some(val => 
          String(val).toLowerCase().includes(search.toLowerCase())
        )
      );
    }
    return rows;
  }, [inventorySubtype, search]);

  const totalRows = filteredRows.length;
  const pagedRows = filteredRows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);

  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left border-collapse">
          <thead>
            {inventorySubtype === "Stock Movement" ? (
              <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
                <Th>Date</Th><Th>Product</Th><Th>Movement Type</Th><Th>Quantity</Th><Th>Branch</Th>
              </tr>
            ) : (
              <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
                <Th>Product</Th><Th>Batch No.</Th><Th>Expiry Date</Th><Th>Quantity</Th><Th>Status</Th>
              </tr>
            )}
          </thead>
          <tbody className="text-[14px] text-[#424751]">
            {pagedRows.length > 0 ? (
              pagedRows.map((row, idx) => {
                const bg = idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]";
                
                if (inventorySubtype === "Stock Movement") {
                  return (
                    <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                      <Td className="text-[#121c2a]">{row.date}</Td>
                      <Td>{row.product}</Td>
                      <Td>{row.type}</Td>
                      <Td className="font-bold text-[#121c2a]">{row.qty}</Td>
                      <Td>{row.branch}</Td>
                    </tr>
                  );
                } else {
                  let badgeClass = "bg-[#94f7b9] text-[#006d40]";
                  if (row.status === "Expiring Soon") badgeClass = "bg-[#ffdad6] text-[#ba1a1a]";
                  if (row.status === "Expired") badgeClass = "bg-[#ffdad6] text-[#ba1a1a]";
                  return (
                    <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                      <Td className="text-[#121c2a]">{row.product}</Td>
                      <Td>{row.batch}</Td>
                      <Td>{row.expiry}</Td>
                      <Td className="font-bold text-[#121c2a]">{row.qty}</Td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${badgeClass}`}>{row.status}</span>
                      </td>
                    </tr>
                  );
                }
              })
            ) : (
              <tr>
                <td colSpan={5} className="py-8 text-center text-[#424751]">No records found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <Pagination page={page} totalRows={totalRows} onPageChange={setPage} rowsPerPage={ROWS_PER_PAGE} />
    </div>
  );
}

// Main default export
export default function InventoryTab({ inventorySubtype, page, setPage, search }) {
  return (
    <>
      <InventoryStats />
      <InventoryTable inventorySubtype={inventorySubtype} page={page} setPage={setPage} search={search} />
    </>
  );
}
