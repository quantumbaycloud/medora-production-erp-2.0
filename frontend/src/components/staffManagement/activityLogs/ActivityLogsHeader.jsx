import { Download, ScrollText } from "lucide-react";

const ActivityLogsHeader = () => {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-blue-500 to-cyan-500 p-6 shadow-lg sm:p-8">
      {/* Decorative circles */}
      <div className="pointer-events-none absolute -right-8 -top-8 h-40 w-40 rounded-full bg-surface-container-lowest/10 blur-2xl" />
      <div className="pointer-events-none absolute -bottom-10 right-24 h-32 w-32 rounded-full bg-surface-container-lowest/5 blur-xl" />

      <div className="relative flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-surface-container-lowest/15 backdrop-blur-sm ring-1 ring-on-primary/20">
            <ScrollText size={28} className="text-on-primary" />
          </div>
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-on-primary">
              Activity Logs
            </h2>
            <p className="mt-1 text-sm text-blue-50/90">
              Track every action performed by staff in real-time.
            </p>
          </div>
        </div>

        <button
          type="button"
          className="inline-flex items-center gap-2 rounded-xl bg-surface-container-lowest px-5 py-2.5 text-sm font-semibold text-indigo-700 shadow-md transition-all duration-200 hover:shadow-lg hover:brightness-95 active:scale-[0.98]"
        >
          <Download size={18} />
          Export CSV
        </button>
      </div>
    </div>
  );
};

export default ActivityLogsHeader;