import { UserCheck, Clock, AlertTriangle } from "lucide-react";

const STATS = [
  {
    label: "Attendance Rate",
    value: "94.2%",
    icon: UserCheck,
    iconClass: "bg-secondary text-on-primary shadow-lg shadow-secondary-container",
    accentClass: "text-secondary",
    barClass: "bg-secondary"
  },
  {
    label: "Average Check-in",
    value: "08:12 AM",
    icon: Clock,
    iconClass: "bg-primary text-on-primary shadow-lg shadow-primary-fixed",
    accentClass: "text-primary",
    barClass: "bg-primary"
  },
  {
    label: "Today's Absence",
    value: "08 Staff",
    icon: AlertTriangle,
    iconClass: "bg-error text-on-primary shadow-lg shadow-error-container",
    accentClass: "text-error",
    barClass: "bg-error"
  }
];

const AttendanceStatsCards = () => {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {STATS.map((stat) => {
        const Icon = stat.icon;

        return (
          <div
            key={stat.label}
            className="group relative overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="pointer-events-none absolute -right-6 -top-6 h-24 w-24 rounded-full bg-primary-fixed opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

            <div className="relative flex items-center gap-4">
              <div
                className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl ${stat.iconClass}`}
              >
                <Icon size={26} strokeWidth={2.2} />
              </div>
              <div className="flex-1">
                <p className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  {stat.label}
                </p>
                <h4 className={`text-2xl font-bold ${stat.accentClass}`}>
                  {stat.value}
                </h4>
              </div>
            </div>

            <div className="relative mt-4 h-1 w-full overflow-hidden rounded-full bg-surface-container">
              <div className={`h-full w-3/4 rounded-full ${stat.barClass}`} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AttendanceStatsCards;