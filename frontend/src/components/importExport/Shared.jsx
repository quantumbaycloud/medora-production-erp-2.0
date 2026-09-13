import { AlertCircle, CheckCircle, XCircle, X } from "lucide-react";

export function Th({ children, className = "" }) {
  return (
    <th
      className={`py-3 px-4 text-[12px] uppercase tracking-wider font-semibold border-b border-[#c2c6d3] ${className}`}
    >
      {children}
    </th>
  );
}

export function Td({ children, className = "", isError = false }) {
  if (isError) {
    return (
      <td className={`py-3 px-4 text-[#ba1a1a] ${className}`}>
        <span className="flex items-center gap-1">
          <AlertCircle size={14} className="text-[#ba1a1a] shrink-0" />
          {children}
        </span>
      </td>
    );
  }
  return <td className={`py-3 px-4 ${className}`}>{children}</td>;
}

export function StatusBadge({ status }) {
  const config = {
    Completed: { bg: "bg-[#94f7b9]", text: "text-[#006d40]", icon: CheckCircle },
    Failed: { bg: "bg-[#ffdad6]", text: "text-[#ba1a1a]", icon: XCircle },
  };
  const { bg, text, icon: Icon } = config[status] || config.Completed;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${bg} ${text}`}>
      <Icon size={12} />
      {status}
    </span>
  );
}

export function Toast({ title, message, icon: Icon, onClose }) {
  return (
    <div className="fixed top-20 right-6 bg-white border border-[#c2c6d3] shadow-lg rounded-lg p-4 flex items-center gap-3 z-50 max-w-sm animate-in slide-in-from-top-2 fade-in duration-300">
      <div className="bg-[#94f7b9] p-2 rounded-full text-[#006d40] shrink-0">
        <Icon size={20} />
      </div>
      <div>
        <h4 className="text-sm font-semibold text-[#121c2a]">{title}</h4>
        <p className="text-xs text-[#424751]">{message}</p>
      </div>
      <button className="ml-auto text-[#424751] hover:text-[#121c2a] transition" onClick={onClose}>
        <X size={18} />
      </button>
    </div>
  );
}
