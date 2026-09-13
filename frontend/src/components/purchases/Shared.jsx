import { ChevronDown, CheckCircle, AlertTriangle, Info, X } from "lucide-react";

export function StatCard({ label, value, subtext, icon: Icon, iconColor = "text-[#004287]" }) {
  return (
    <div className="bg-white rounded border border-[#c2c6d3] p-6 hover:border-[#004287] transition-colors flex flex-col">
      <div className="flex items-center justify-between mb-2">
        <div className="font-label-md uppercase tracking-wider text-[#424751]">{label}</div>
        {Icon && <Icon size={18} className={iconColor} />}
      </div>
      <div className="font-headline-lg font-bold text-[#121c2a]">{value}</div>
      {subtext && <div className="mt-2 text-sm text-[#424751]">{subtext}</div>}
    </div>
  );
}

export function Pagination({ page, totalRows, onPageChange, pageSize = 5 }) {
  const totalPages = Math.max(Math.ceil(totalRows / pageSize), 1);
  const startIdx = (page - 1) * pageSize;
  const endIdx = Math.min(startIdx + pageSize, totalRows);
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
          <ChevronDown className="rotate-90" size={18} />
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
          <ChevronDown className="-rotate-90" size={18} />
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

// toastType: "success" | "error" | "info"
export function Toast({ type = "success", title, message, onClose }) {
  const config = {
    success: { bg: "bg-[#94f7b9]", text: "text-[#006d40]", icon: CheckCircle, label: "Success" },
    error: { bg: "bg-[#ffdad6]", text: "text-[#ba1a1a]", icon: AlertTriangle, label: "Error" },
    info: { bg: "bg-[#d6e3ff]", text: "text-[#004287]", icon: Info, label: "Info" },
  };
  const { bg, text, icon: Icon, label } = config[type] || config.success;
  return (
    <div className="fixed top-[80px] right-6 bg-white border border-[#c2c6d3] shadow-lg rounded-lg p-4 flex items-center gap-3 z-50 max-w-sm animate-in slide-in-from-top-2 fade-in duration-300">
      <div className={`p-2 rounded-full flex-shrink-0 ${bg} ${text}`}>
        <Icon size={20} />
      </div>
      <div>
        <h4 className="text-sm font-semibold text-[#121c2a]">{title || label}</h4>
        <p className="text-xs text-[#424751]">{message}</p>
      </div>
      <button className="ml-auto text-[#424751] hover:text-[#121c2a] transition" onClick={onClose}>
        <X size={18} />
      </button>
    </div>
  );
}
