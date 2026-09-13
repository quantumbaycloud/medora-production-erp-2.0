import { useMemo } from "react";
import { supplierData, STAT_LABELS, ROWS_PER_PAGE } from "../../data/reports/data";
import { StatCard, Pagination, Th, Td } from "./Shared";

// Stats Component
export function SupplierStats() {
  const [label1, label2, label3] = STAT_LABELS.supplier;

  const stats = [
    { value: supplierData.stats.totalSuppliers, icon: "arrow_upward", text: "Active suppliers", cls: "text-[#006d40]" },
    { value: supplierData.stats.outstanding, icon: "trending_up", text: "needs settlement", cls: "text-[#006d40]" },
    { value: supplierData.stats.deliveryRate, icon: "info", text: "Delivery performance", cls: "text-[#424751]" },
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
export function SupplierTable({ supplierFilter, page, setPage, search }) {
  const filteredRows = useMemo(() => {
    let rows = supplierData.rows;
    if (supplierFilter !== "All Suppliers") {
      if (supplierFilter === "Has Outstanding") {
        rows = rows.filter((r) => r.outstanding !== "₹0");
      } else if (supplierFilter === "Fully Paid") {
        rows = rows.filter((r) => r.outstanding === "₹0");
      }
    }
    if (search) {
      rows = rows.filter((r) => 
        r.name.toLowerCase().includes(search.toLowerCase())
      );
    }
    return rows;
  }, [supplierFilter, search]);

  const totalRows = filteredRows.length;
  const pagedRows = filteredRows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);

  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left border-collapse">
          <thead>
            <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
              <Th>Supplier Name</Th><Th>Total Supplied</Th><Th>Last Order</Th><Th>Outstanding Amount</Th>
            </tr>
          </thead>
          <tbody className="text-[14px] text-[#424751]">
            {pagedRows.length > 0 ? (
              pagedRows.map((row, idx) => {
                const bg = idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]";
                const outstandingColor = row.outstanding === "₹0" ? "text-[#006d40]" : "text-[#ba1a1a]";
                return (
                  <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                    <Td className="text-[#121c2a]">{row.name}</Td>
                    <Td>{row.totalSupplied}</Td>
                    <Td>{row.lastOrder}</Td>
                    <Td className={`font-bold ${outstandingColor}`}>{row.outstanding}</Td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={4} className="py-8 text-center text-[#424751]">No records found.</td>
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
export default function SupplierTab({ supplierFilter, page, setPage, search }) {
  return (
    <>
      <SupplierStats />
      <SupplierTable supplierFilter={supplierFilter} page={page} setPage={setPage} search={search} />
    </>
  );
}
