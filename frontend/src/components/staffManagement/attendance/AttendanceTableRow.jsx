import { MoreVertical } from "lucide-react";
import AttendanceStatusBadge from "./AttendanceStatusBadge";

const AttendanceTableRow = ({ record }) => {
  return (
    <tr className="group transition-all duration-200 hover:bg-gradient-to-r hover:from-blue-50/60 hover:to-teal-50/40">
      <td className="px-6 py-4 font-mono text-sm text-outline">
        {record.id}
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 shrink-0 overflow-hidden rounded-full bg-gradient-to-br from-blue-100 to-teal-100 p-0.5 ring-2 ring-primary-fixed">
            <img
              src={record.avatar}
              alt={record.name}
              className="h-full w-full rounded-full object-cover"
            />
          </div>
          <div>
            <p className="text-sm font-bold text-on-background">{record.name}</p>
            <p className="text-xs text-on-surface-variant">{record.department}</p>
          </div>
        </div>
      </td>
      <td className="px-6 py-4 text-sm text-on-surface-variant">{record.date}</td>
      <td className="px-6 py-4 font-mono text-sm font-medium text-primary">
        {record.checkIn}
      </td>
      <td className="px-6 py-4 font-mono text-sm font-medium text-teal-700">
        {record.checkOut}
      </td>
      <td className="px-6 py-4">
        <span className="inline-flex items-center rounded-lg bg-surface-container-low px-2.5 py-1 font-mono text-xs font-semibold text-on-surface-variant ring-1 ring-outline-variant">
          {record.workingHours}
        </span>
      </td>
      <td className="px-6 py-4">
        <AttendanceStatusBadge status={record.status} />
      </td>
      <td className="px-6 py-4 text-right">
        <button
          type="button"
          aria-label={`Actions for ${record.name}`}
          className="rounded-lg p-1.5 text-outline transition-all duration-200 hover:bg-primary-fixed hover:text-primary"
        >
          <MoreVertical size={18} />
        </button>
      </td>
    </tr>
  );
};

export default AttendanceTableRow;