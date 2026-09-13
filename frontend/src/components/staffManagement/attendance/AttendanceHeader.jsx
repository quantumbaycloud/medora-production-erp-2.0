import { Download, CalendarCheck2 } from "lucide-react";

const AttendanceHeader = () => {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-primary p-6 shadow-lg sm:p-8">
      {/* Decorative circles */}
      <div className="pointer-events-none absolute -right-8 -top-8 h-40 w-40 rounded-full bg-surface-container-lowest/10 blur-2xl" />
      <div className="pointer-events-none absolute -bottom-10 right-24 h-32 w-32 rounded-full bg-surface-container-lowest/5 blur-xl" />

      <div className="relative flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-surface-container-lowest/15 backdrop-blur-sm ring-1 ring-on-primary/20">
            <CalendarCheck2 size={28} className="text-on-primary" />
          </div>
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-on-primary">
              Attendance
            </h2>
            <p className="mt-1 text-sm text-blue-50/90">
              Track staff daily attendance
            </p>
          </div>
        </div>

        <button
          type="button"
          className="inline-flex items-center gap-2 rounded-xl bg-surface-container-lowest px-5 py-2.5 text-sm font-semibold text-primary shadow-md transition-all duration-200 hover:shadow-lg hover:brightness-95 active:scale-95"
        >
          <Download size={18} />
          Export Records
        </button>
      </div>
    </div>
  );
};

export default AttendanceHeader;