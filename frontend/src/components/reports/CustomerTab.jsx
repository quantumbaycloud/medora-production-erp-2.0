import { useMemo } from "react";
import { customerData, STAT_LABELS, ROWS_PER_PAGE } from "../../data/reports/data";
import { StatCard, Pagination, Th, Td } from "./Shared";

// Stats Component
export function CustomerStats() {
  const [label1, label2, label3] = STAT_LABELS.customer;

  const stats = [
    { value: customerData.stats.customers, icon: "arrow_upward", text: "5.4% vs previous period", cls: "text-[#006d40]" },
    { value: customerData.stats.revenue, icon: "trending_up", text: "growing", cls: "text-[#006d40]" },
    { value: customerData.stats.repeatRate, icon: "info", text: "Loyalty metric", cls: "text-[#424751]" },
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
export function CustomerTable({ customerType, page, setPage, search }) {
  const filteredRows = useMemo(() => {
    let rows = customerData.rows;
    if (customerType !== "All Customers") rows = rows.filter((r) => r.type === customerType);
    if (search) {
      rows = rows.filter((r) => 
        r.name.toLowerCase().includes(search.toLowerCase()) ||
        r.type.toLowerCase().includes(search.toLowerCase())
      );
    }
    return rows;
  }, [customerType, search]);

  const totalRows = filteredRows.length;
  const pagedRows = filteredRows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);

  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left border-collapse">
          <thead>
            <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
              <Th>Name</Th><Th>Orders</Th><Th>Spend</Th><Th>Last Purchase</Th>
            </tr>
          </thead>
          <tbody className="text-[14px] text-[#424751]">
            {pagedRows.length > 0 ? (
              pagedRows.map((row, idx) => {
                const bg = idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]";
                return (
                  <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                    <Td className="text-[#121c2a]">{row.name}</Td>
                    <Td>{row.orders}</Td>
                    <Td className="font-bold text-[#121c2a]">{row.spend}</Td>
                    <Td>{row.lastPurchase}</Td>
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
export default function CustomerTab({ customerType, page, setPage, search }) {
  return (
    <>
      <CustomerStats />
      <CustomerTable customerType={customerType} page={page} setPage={setPage} search={search} />
    </>
  );
}