import { useMemo } from "react";
import { purchaseData, STAT_LABELS, ROWS_PER_PAGE } from "../../data/reports/data";
import { StatCard, Pagination, Th, Td } from "./Shared";

// Stats Component
export function PurchaseStats() {
  const [label1, label2, label3] = STAT_LABELS.purchase;

  const stats = [
    { value: purchaseData.stats.total, icon: "arrow_upward", text: "3.1% vs last month", cls: "text-[#006d40]" },
    { value: purchaseData.stats.amount, icon: "trending_up", text: "on track", cls: "text-[#006d40]" },
    { value: purchaseData.stats.pending, icon: "info", text: "Needs follow-up", cls: "text-[#424751]" },
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
export function PurchaseTable({ status, supplier, page, setPage, search }) {
  const filteredRows = useMemo(() => {
    let rows = purchaseData.rows;
    if (status !== "All Status") rows = rows.filter((r) => r.status === status);
    if (supplier !== "All Suppliers") rows = rows.filter((r) => r.supplier === supplier);
    if (search) {
      rows = rows.filter((r) => 
        r.supplier.toLowerCase().includes(search.toLowerCase()) ||
        r.status.toLowerCase().includes(search.toLowerCase())
      );
    }
    return rows;
  }, [status, supplier, search]);

  const totalRows = filteredRows.length;
  const pagedRows = filteredRows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);

  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left border-collapse">
          <thead>
            <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
              <Th>Supplier</Th><Th>Date</Th><Th>Items</Th><Th>Amount</Th><Th>Status</Th>
            </tr>
          </thead>
          <tbody className="text-[14px] text-[#424751]">
            {pagedRows.length > 0 ? (
              pagedRows.map((row, idx) => {
                const bg = idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]";
                return (
                  <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                    <Td>{row.supplier}</Td>
                    <Td className="text-[#121c2a]">{row.date}</Td>
                    <Td>{row.items}</Td>
                    <Td className="font-bold text-[#121c2a]">{row.amount}</Td>
                    <Td>
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        row.status === "Delivered" ? "bg-[#94f7b9] text-[#006d40]" :
                        row.status === "Pending" ? "bg-[#ffdad6] text-[#ba1a1a]" :
                        "bg-[#d6e3ff] text-[#004287]"
                      }`}>
                        {row.status}
                      </span>
                    </Td>
                  </tr>
                );
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
export default function PurchaseTab({ status, supplier, page, setPage, search }) {
  return (
    <>
      <PurchaseStats />
      <PurchaseTable status={status} supplier={supplier} page={page} setPage={setPage} search={search} />
    </>
  );
}
