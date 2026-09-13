import { TrendingUp } from "lucide-react";

const ActivityLogsStatsCards = () => {
  return (
    <div className="grid grid-cols-1 gap-6">
      {/* Weekly Trend */}
      <div className="group relative col-span-1 overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
        {/* Decorative gradient blob */}
        <div className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full bg-gradient-to-br from-indigo-100 to-cyan-100 opacity-60 transition-opacity duration-300 group-hover:opacity-100" />

        <div className="relative flex items-center gap-6">
          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-500 text-on-primary shadow-lg shadow-indigo-200">
            <TrendingUp size={32} strokeWidth={2.2} />
          </div>
          <div>
            <h4 className="text-xl font-bold text-on-background">Weekly Trend</h4>
            <p className="mt-1 text-base text-on-surface-variant">
              There is a{" "}
              <span className="font-semibold text-secondary">12% increase</span>{" "}
              in staff check-ins compared to last week.
            </p>
          </div>
        </div>

        {/* Mini trend bars */}
        <div className="relative mt-5 flex items-end gap-1.5">
          {[35, 50, 42, 65, 58, 78, 90].map((height, index) => (
            <div
              key={index}
              className="w-full rounded-t-md bg-gradient-to-t from-indigo-200 to-cyan-300 transition-all duration-300 group-hover:from-indigo-400 group-hover:to-cyan-400"
              style={{ height: `${height * 0.4}px` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ActivityLogsStatsCards;