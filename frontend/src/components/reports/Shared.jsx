import { ChevronLeft, ChevronRight, ArrowUp, TrendingUp, Info } from "lucide-react";

export function StatCard({ label, value, trendIcon, trendText, trendClass }) {
  return (
    <div className="bg-white rounded border border-[#c2c6d3] p-6 hover:border-[#004287] transition-colors">
      <div className="font-label-md uppercase tracking-wider mb-2 text-[#424751]">{label}</div>
      <div className="font-headline-lg font-bold text-[#121c2a]">{value}</div>
      <div className={`mt-4 flex items-center gap-1 font-label-md ${trendClass}`}>
        {trendIcon === "arrow_upward" && <ArrowUp size={16} />}
        {trendIcon === "trending_up" && <TrendingUp size={16} />}
        {trendIcon === "info" && <Info size={16} />}
        <span>{trendText}</span>
      </div>
    </div>
  );
}

export function Pagination({ page, totalRows, onPageChange, rowsPerPage = 5 }) {
  const totalPages = Math.max(Math.ceil(totalRows / rowsPerPage), 1);
  const startIdx = (page - 1) * rowsPerPage;
  const endIdx = Math.min(startIdx + rowsPerPage, totalRows);
  const startDisplay = totalRows === 0 ? 0 : startIdx + 1;

  const pages = [];
  for (let p = 1; p <= Math.min(totalPages, 3); p++) pages.push(p);

  return (
    <div className="bg-white border-t border-[#c2c6d3] p-4 flex items-center justify-between rounded-b">
      <div className="font-label-md text-[#424751]">
        Showing <span className="font-bold text-[#121c2a]">{startDisplay}-{endIdx}</span> of{" "}
        <span className="font-bold text-[#121c2a]">{totalRows}</span> entries
      </div>
      <div className="flex items-center gap-2 ml-auto">
        <button
          disabled={page === 1}
          onClick={() => onPageChange(page - 1)}
          className="p-1 rounded border border-[#c2c6d3] text-[#424751] hover:border-[#004287] hover:text-[#004287] disabled:opacity-50 transition-colors"
        >
          <ChevronLeft size={18} />
        </button>
        {pages.map((p) => (
          <button
            key={p}
            onClick={() => onPageChange(p)}
            className={`w-8 h-8 rounded font-label-md font-bold flex items-center justify-center transition-colors ${
              p === page
                ? "bg-[#004287] text-white border border-[#004287]"
                : "bg-transparent border border-[#c2c6d3] text-[#121c2a] hover:bg-[#eff4ff]"
            }`}
          >
            {p}
          </button>
        ))}
        <button
          disabled={page === totalPages}
          onClick={() => onPageChange(page + 1)}
          className="p-1 rounded border border-[#c2c6d3] text-[#424751] hover:border-[#004287] hover:text-[#004287] disabled:opacity-50 transition-colors"
        >
          <ChevronRight size={18} />
        </button>
      </div>
    </div>
  );
}

export function Th({ children, className = "" }) {
  return (
    <th className={`py-3 px-4 text-[12px] uppercase tracking-wider font-semibold border-b border-[#c2c6d3] ${className}`}>
      {children}
    </th>
  );
}

export function Td({ children, className = "" }) {
  return <td className={`py-3 px-4 ${className}`}>{children}</td>;
}
