import { Download, FilePlus2 } from "lucide-react";

const DashboardHeader = () => {
  return (
    <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
      <div>
        <p className="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-primary">
          Pharmacy dashboard
        </p>
        <h2 className="text-3xl font-bold tracking-tight text-on-background md:text-4xl">
          Today at a glance
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-on-surface-variant">
          Monitor sales, orders, and inventory health across every active branch.
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          className="flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-on-primary shadow-sm transition-colors hover:bg-primary-container"
        >
          <FilePlus2 size={18} />
          New Prescription
        </button>
        <button
          type="button"
          className="flex items-center justify-center gap-2 rounded-lg border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-sm font-semibold text-on-surface transition-colors hover:bg-surface-container-low"
        >
          <Download size={18} />
          Export Data
        </button>
      </div>
    </div>
  );
};

export default DashboardHeader;
