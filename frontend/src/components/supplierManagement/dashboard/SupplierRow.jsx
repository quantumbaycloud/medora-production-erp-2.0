import { Link } from "react-router-dom";
import { Eye } from "lucide-react";

const SupplierRow = ({ supplier, index }) => {
  return (
    <tr
      className={`group border-b border-slate-100 transition-colors hover:bg-primary-fixed/30 ${
        index % 2 !== 0 ? "bg-[#F8FCFF]/50" : ""
      }`}
    >
      <td className="p-4">
        <div className="flex items-center gap-3">
          <div
            className={`flex h-9 w-9 items-center justify-center rounded-xl text-sm font-bold shadow-sm ${supplier.avatarBg} ${supplier.avatarText}`}
          >
            {supplier.initial}
          </div>

          <span className="font-semibold text-on-background">{supplier.name}</span>
        </div>
      </td>

      <td className="p-4 text-sm text-on-surface-variant">
        {supplier.contact}
      </td>

      <td className="p-4 text-right font-mono text-sm font-semibold text-on-background">
        {supplier.balance}
      </td>

      <td className="p-4 text-center">
        <span
          className={`inline-flex rounded-full px-2.5 py-1 text-[11px] font-medium ${supplier.statusClass}`}
        >
          {supplier.status}
        </span>
      </td>

      <td className="p-4 text-right">
        <Link
          to={`/suppliers/${supplier.id}`}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-3.5 py-2 text-xs font-semibold text-on-primary shadow-sm transition hover:opacity-95 hover:shadow-md"
        >
          <Eye size={13} />
          <span>View Details</span>
        </Link>
      </td>
    </tr>
  );
};

export default SupplierRow;
