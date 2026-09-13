import {
  Building2,
  Pencil,
  ShoppingCart,
  TrendingUp,
  TriangleAlert,
} from "lucide-react";
import { branchDeepDive } from "../../../data/pharmacySettings/pharmacySettingsData";

const statIconMap = {
  "trending-up": TrendingUp,
  "shopping-cart": ShoppingCart,
  "triangle-alert": TriangleAlert,
};

const statToneMap = {
  primary: "bg-primary/10 text-primary",
  neutral: "bg-surface-container-high text-on-surface-variant",
  error: "bg-error-container text-on-error-container",
};

const ToggleRow = ({ label, enabled }) => (
  <div className="flex items-center justify-between">
    <span className="text-sm text-on-surface">{label}</span>
    <span
      role="switch"
      aria-checked={enabled}
      aria-label={label}
      className={`relative inline-flex h-5 w-10 items-center rounded-full px-1 ${
        enabled ? "bg-primary" : "bg-outline-variant"
      }`}
    >
      <span
        className={`h-3.5 w-3.5 rounded-full bg-white transition-transform ${
          enabled ? "translate-x-5" : "translate-x-0"
        }`}
      />
    </span>
  </div>
);

const ConfigItem = ({ label, value }) => (
  <div>
    <p className="mb-1 text-xs font-semibold text-on-surface-variant">{label}</p>
    <p className="text-sm font-bold text-on-background">{value}</p>
  </div>
);

const BranchDeepDive = () => (
  <section className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
    <div className="flex flex-col justify-between gap-3 bg-primary px-8 py-4 text-on-primary md:flex-row md:items-center">
      <div className="flex items-center gap-3">
        <Building2 size={26} />
        <h3 className="text-lg font-bold">Branch Deep-Dive: {branchDeepDive.name}</h3>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-xs italic opacity-80">{branchDeepDive.lastAudit}</span>
        <button
          type="button"
          aria-label="Edit branch"
          className="rounded-lg bg-white/20 p-2 transition-colors hover:bg-white/30"
        >
          <Pencil size={16} />
        </button>
      </div>
    </div>

    <div className="grid grid-cols-1 gap-8 p-8 lg:grid-cols-12">
      <div className="space-y-6 lg:col-span-3">
        <h4 className="border-b border-outline-variant pb-2 text-xs font-bold uppercase tracking-widest text-on-surface-variant">
          Branch Statistics
        </h4>
        <div className="space-y-4">
          {branchDeepDive.statistics.map(({ label, value, icon, tone }) => {
            const Icon = statIconMap[icon] ?? TrendingUp;

            return (
              <div
                key={label}
                className="flex items-center justify-between rounded-xl border border-outline-variant bg-surface p-4"
              >
                <div>
                  <p className="text-xs font-semibold text-on-surface-variant">{label}</p>
                  <p
                    className={`text-xl font-bold ${tone === "error" ? "text-error" : "text-on-background"}`}
                  >
                    {value}
                  </p>
                </div>
                <span className={`rounded-lg p-2 ${statToneMap[tone]}`}>
                  <Icon size={18} />
                </span>
              </div>
            );
          })}
        </div>
      </div>

      <div className="space-y-6 lg:col-span-6">
        <h4 className="border-b border-outline-variant pb-2 text-xs font-bold uppercase tracking-widest text-on-surface-variant">
          Configuration & Settings
        </h4>

        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-4">
            {branchDeepDive.toggles.map(({ label, enabled }) => (
              <ToggleRow key={label} label={label} enabled={enabled} />
            ))}
          </div>
          <div className="space-y-4">
            <ConfigItem label="Currency" value={branchDeepDive.configuration.currency} />
            <ConfigItem label="Tax Scheme" value={branchDeepDive.configuration.taxScheme} />
            <ConfigItem
              label="Operating Hours"
              value={branchDeepDive.configuration.operatingHours}
            />
          </div>
        </div>

        <div className="flex gap-3 rounded-xl border border-outline-variant bg-surface p-4">
          <TriangleAlert size={18} className="mt-0.5 shrink-0 text-primary" />
          <div>
            <p className="text-xs font-bold text-on-background">Branch Location</p>
            <p className="text-sm text-on-surface-variant">
              {branchDeepDive.configuration.location}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6 lg:col-span-3">
        <h4 className="border-b border-outline-variant pb-2 text-xs font-bold uppercase tracking-widest text-on-surface-variant">
          Status Timeline
        </h4>
        <ol className="relative space-y-6 border-l-2 border-outline-variant pl-6">
          {branchDeepDive.timeline.map(({ event, timestamp, current }) => (
            <li key={event} className={`relative ${current ? "" : "opacity-60"}`}>
              <span
                className={`absolute -left-[31px] top-1 h-4 w-4 rounded-full ring-4 ring-surface-container-lowest ${
                  current ? "bg-primary" : "bg-outline-variant"
                }`}
              />
              <p className="text-xs font-bold text-on-background">{event}</p>
              <p className="text-[10px] text-on-surface-variant">{timestamp}</p>
            </li>
          ))}
        </ol>
      </div>
    </div>
  </section>
);

export default BranchDeepDive;