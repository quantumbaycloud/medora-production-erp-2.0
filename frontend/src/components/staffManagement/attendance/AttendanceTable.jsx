import { ChevronLeft, ChevronRight } from "lucide-react";
import AttendanceTableRow from "./AttendanceTableRow";

const AttendanceTable = ({ records }) => {
  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="bg-primary text-[11px] font-bold uppercase tracking-widest text-on-primary">
              <th className="px-6 py-4">#</th>
              <th className="px-6 py-4">Employee Name</th>
              <th className="px-6 py-4">Date</th>
              <th className="px-6 py-4">Check In</th>
              <th className="px-6 py-4">Check Out</th>
              <th className="px-6 py-4">Working Hours</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {records.map((record) => (
              <AttendanceTableRow key={record.id} record={record} />
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex flex-col gap-4 border-t border-outline-variant bg-gradient-to-r from-slate-50 to-blue-50/40 px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-on-surface-variant">
          Showing <span className="font-bold text-primary">{records.length}</span> of{" "}
          <span className="font-bold text-primary">124</span> records
        </p>
        <div className="flex items-center gap-1">
          <button
            type="button"
            aria-label="Previous page"
            disabled
            className="rounded-lg p-2 text-outline transition-colors hover:bg-surface-container hover:text-on-surface-variant disabled:opacity-40 disabled:hover:bg-transparent"
          >
            <ChevronLeft size={18} />
          </button>
          <button
            type="button"
            className="h-8 w-8 rounded-lg bg-primary text-sm font-semibold text-on-primary shadow-sm"
          >
            1
          </button>
          <button
            type="button"
            className="h-8 w-8 rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-primary-fixed hover:text-primary"
          >
            2
          </button>
          <button
            type="button"
            className="h-8 w-8 rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-primary-fixed hover:text-primary"
          >
            3
          </button>
          <span className="px-2 text-sm text-outline">...</span>
          <button
            type="button"
            className="h-8 w-8 rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-primary-fixed hover:text-primary"
          >
            25
          </button>
          <button
            type="button"
            aria-label="Next page"
            className="rounded-lg p-2 text-on-surface-variant transition-colors hover:bg-primary-fixed hover:text-primary"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default AttendanceTable;