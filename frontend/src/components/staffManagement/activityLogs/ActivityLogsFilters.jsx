import { User, Filter, CalendarDays, RotateCcw } from "lucide-react";

const ActivityLogsFilters = () => {
  return (
    <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-indigo-100 bg-surface-container-lowest/80 p-4 shadow-sm backdrop-blur">
      {/* Search Employee */}
      <div className="relative min-w-[240px] flex-1">
        <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-indigo-400" />
        <input
          type="text"
          placeholder="Search employee name..."
          className="w-full rounded-xl border border-indigo-100 bg-gradient-to-r from-slate-50 to-indigo-50/30 py-2 pl-9 pr-3 text-sm text-on-surface-variant outline-none transition-all duration-200 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/20"
        />
      </div>

      {/* Action Type */}
      <div className="flex min-w-[200px] items-center gap-2">
        <Filter size={16} className="shrink-0 text-blue-400" />
        <select
          className="w-full cursor-pointer rounded-xl border border-blue-100 bg-gradient-to-r from-slate-50 to-blue-50/30 px-3 py-2 text-sm text-on-surface-variant outline-none transition-all duration-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20"
          defaultValue=""
        >
          <option value="">All Action Types</option>
          <option value="create">Created Resource</option>
          <option value="update">Updated Information</option>
          <option value="delete">Deleted Record</option>
          <option value="login">Authentication</option>
        </select>
      </div>

      {/* Date */}
      <div className="flex min-w-[200px] items-center gap-2">
        <CalendarDays size={16} className="shrink-0 text-cyan-500" />
        <input
          type="date"
          className="w-full rounded-xl border border-cyan-100 bg-gradient-to-r from-slate-50 to-cyan-50/30 px-3 py-2 text-sm text-on-surface-variant outline-none transition-all duration-200 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
        />
      </div>

      {/* Reset */}
      <button
        type="button"
        className="inline-flex items-center gap-1.5 rounded-xl border border-outline-variant bg-surface-container-lowest px-4 py-2 text-sm font-semibold text-on-surface-variant shadow-sm transition-all duration-200 hover:border-rose-200 hover:bg-error-container hover:text-error"
      >
        <RotateCcw size={14} />
        Reset
      </button>
    </div>
  );
};

export default ActivityLogsFilters;