import { useMemo } from "react";
import { MoreVertical } from "lucide-react";
import { salesData, STAT_LABELS, ROWS_PER_PAGE } from "../../data/reports/data";
import { StatCard, Pagination, Th, Td } from "./Shared";

// Stats Component
export function SalesStats({ period }) {
  const [label1, label2, label3] = STAT_LABELS.sales;
  
  const stats = useMemo(() => {
    const s = salesData[period].stats;
    return [
      { value: s.sales, icon: "arrow_upward", text: s.salesTrend, cls: "text-[#006d40]" },
      { value: s.revenue, icon: "trending_up", text: s.revenueTrend, cls: "text-[#006d40]" },
      { value: s.transactions, icon: "info", text: "Aggregated transactions", cls: "text-[#424751]" },
    ];
  }, [period]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard label={label1} value={stats[0].value} trendIcon={stats[0].icon} trendText={stats[0].text} trendClass={stats[0].cls} />
      <StatCard label={label2} value={stats[1].value} trendIcon={stats[1].icon} trendText={stats[1].text} trendClass={stats[1].cls} />
      <StatCard label={label3} value={stats[2].value} trendIcon={stats[2].icon} trendText={stats[2].text} trendClass={stats[2].cls} />
    </div>
  );
}

// Table Component
export function SalesTable({ period, branch, page, setPage, search }) {
  const filteredRows = useMemo(() => {
    let rows = salesData[period].rows;
    if (branch !== "All Branches") rows = rows.filter((r) => r.branch === branch);
    if (search) rows = rows.filter((r) => 
      r.date.toLowerCase().includes(search.toLowerCase()) ||
      r.branch.toLowerCase().includes(search.toLowerCase())
    );
    return rows;
  }, [period, branch, search]);

  const totalRows = filteredRows.length;
  const pagedRows = filteredRows.slice((page - 1) * ROWS_PER_PAGE, page * ROWS_PER_PAGE);

  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left border-collapse">
          <thead>
            <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
              <Th>Date</Th><Th>Branch</Th><Th>Total Sales</Th><Th>Transactions</Th><Th>Revenue</Th>
              <Th className="text-center">Actions</Th>
            </tr>
          </thead>
          <tbody className="text-[14px] text-[#424751]">
            {pagedRows.length > 0 ? (
              pagedRows.map((row, idx) => {
                const bg = idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]";
                return (
                  <tr key={idx} className={`hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3] ${bg}`}>
                    <Td className="text-[#121c2a]">{row.date}</Td>
                    <Td>{row.branch}</Td>
                    <Td>{row.sales}</Td>
                    <Td>{row.trans}</Td>
                    <Td className="font-bold text-[#121c2a]">{row.rev}</Td>
                    <td className="py-3 px-4 text-center">
                      <button className="text-[#004287] hover:text-[#235eac] transition-colors p-1">
                        <MoreVertical size={18} />
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={6} className="py-8 text-center text-[#424751]">No records found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <Pagination page={page} totalRows={totalRows} onPageChange={setPage} rowsPerPage={ROWS_PER_PAGE} />
    </div>
  );
}

// Main default export (for backward compatibility)
export default function SalesTab({ period, branch, page, setPage, search }) {
  return (
    <>
      <SalesStats period={period} />
      <SalesTable period={period} branch={branch} page={page} setPage={setPage} search={search} />
    </>
  );
}
