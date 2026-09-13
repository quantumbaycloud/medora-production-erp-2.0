import { useState } from "react";
import { revenueOverview } from "../../../data/pharmacySettings/pharmacySettingsData";

const RevenueChart = () => {
  const [activePeriod, setActivePeriod] = useState("Monthly");

  return (
    <section className="rounded-xl border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:p-6">
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-semibold text-on-surface-variant">Revenue trend</p>
          <div className="mt-1 flex items-end gap-3">
            <h4 className="text-3xl font-bold tracking-tight text-on-background">$420.5k</h4>
            <span className="mb-1 rounded-full bg-secondary-container px-2 py-0.5 text-xs font-bold text-on-secondary-fixed-variant">
              +8%
            </span>
          </div>
        </div>
        <div className="flex w-fit items-center rounded-lg bg-surface-container-low p-1">
          {revenueOverview.periods.map((period) => (
            <button
              key={period}
              type="button"
              onClick={() => setActivePeriod(period)}
              aria-pressed={period === activePeriod}
              className={`rounded-md px-3 py-1.5 text-xs font-bold transition-colors ${
                period === activePeriod
                  ? "bg-secondary-container text-on-secondary-fixed-variant shadow-sm"
                  : "text-on-surface-variant hover:text-primary"
              }`}
            >
              {period}
            </button>
          ))}
        </div>
      </div>

      <div className="relative h-[250px] border-b border-outline-variant px-2">
        <div className="absolute inset-0 flex flex-col justify-between pb-6">
          {[1, 2, 3, 4].map((line) => (
            <span key={line} className="border-t border-dashed border-outline-variant/60" />
          ))}
        </div>
        <div className="absolute inset-0 flex items-end gap-3 px-2">
          {revenueOverview.bars.map((height, index) => (
            <div
              key={`${activePeriod}-${index}`}
              className="group flex h-full flex-1 items-end"
            >
              <div
                style={{ height: `${height}%` }}
                className="w-full rounded-t-md bg-primary/35 transition-colors group-hover:bg-primary"
              />
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 text-xs font-medium text-on-surface-variant">
        <span>Start of period</span>
        <span>Current</span>
      </div>
    </section>
  );
};

export default RevenueChart;
