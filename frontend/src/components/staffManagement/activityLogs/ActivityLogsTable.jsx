import { ChevronLeft, ChevronRight } from "lucide-react";
import ActivityLogsTableRow from "./ActivityLogsTableRow";

const ActivityLogsTable = ({ logs }) => {
  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest/80 shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gradient-to-r from-indigo-600 via-blue-500 to-cyan-500 text-[12px] font-bold uppercase tracking-wider text-on-primary">
              <th className="w-16 px-8 py-5 text-left">#</th>
              <th className="px-8 py-5 text-left">Employee Name</th>
              <th className="px-8 py-5 text-left">Action Performed</th>
              <th className="px-8 py-5 text-left">Module</th>
              <th className="px-8 py-5 text-left">Timestamp</th>
              <th className="px-8 py-5 text-center">IP Address</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {logs.map((log) => (
              <ActivityLogsTableRow key={log.id} log={log} />
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex flex-col gap-4 border-t border-outline-variant bg-gradient-to-r from-slate-50 to-indigo-50/40 px-8 py-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-on-surface-variant">
          Showing <span className="font-bold text-indigo-700">1 - {logs.length}</span> of{" "}
          <span className="font-bold text-indigo-700">124</span> results
        </p>
        <div className="flex items-center gap-1">
          <button
            type="button"
            aria-label="Previous page"
            className="rounded-lg p-2 text-outline transition-colors hover:bg-indigo-50 hover:text-indigo-600"
          >
            <ChevronLeft size={18} />
          </button>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-r from-indigo-600 via-blue-500 to-cyan-500 text-sm font-semibold text-on-primary shadow-sm"
          >
            1
          </button>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-indigo-50 hover:text-indigo-700"
          >
            2
          </button>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-indigo-50 hover:text-indigo-700"
          >
            3
          </button>
          <span className="px-2 text-sm text-outline">...</span>
          <button
            type="button"
            className="flex h-9 w-9 items-center justify-center rounded-lg text-sm font-semibold text-on-surface-variant transition-colors hover:bg-indigo-50 hover:text-indigo-700"
          >
            25
          </button>
          <button
            type="button"
            aria-label="Next page"
            className="rounded-lg p-2 text-outline transition-colors hover:bg-indigo-50 hover:text-indigo-600"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ActivityLogsTable;