import { TriangleAlert } from "lucide-react";
import { lowStockAlerts } from "../../../data/pharmacySettings/pharmacySettingsData";

const LowStockPanel = () => (
  <section className="h-full overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:p-6">
    <div className="flex items-start justify-between border-b border-outline-variant pb-5">
      <div>
        <h4 className="text-lg font-bold text-on-background">Critical inventory</h4>
        <p className="mt-1 text-xs text-on-surface-variant">Items that need attention today</p>
      </div>
      <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-error-container text-error">
        <TriangleAlert size={20} />
      </span>
    </div>
    <div className="divide-y divide-outline-variant">
      {lowStockAlerts.map(({ medicine, location, quantity }) => (
        <div key={medicine} className="flex items-center justify-between gap-4 py-5">
          <div>
            <p className="text-sm font-semibold text-on-background">{medicine}</p>
            <p className="mt-1 text-xs text-on-surface-variant">
              {location} · <span className="font-bold text-error">{quantity} remaining</span>
            </p>
          </div>
          <button
            type="button"
            className="rounded-lg border border-outline-variant px-3 py-2 text-xs font-bold text-primary transition-colors hover:border-primary hover:bg-primary-fixed"
          >
            Restock
          </button>
        </div>
      ))}
    </div>
    <button type="button" className="mt-2 text-sm font-bold text-primary hover:underline">
      View inventory alerts
    </button>
  </section>
);

export default LowStockPanel;
