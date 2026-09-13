import {
  AlertTriangle,
  BadgeCheck,
  Building2,
  CalendarX,
  Clock,
  Pill,
  ShoppingBag,
  TrendingDown,
  TrendingUp,
  Users,
  Wallet,
  XCircle,
} from "lucide-react";
import { kpiSummary } from "../../../data/pharmacySettings/pharmacySettingsData";

const featuredMetricIds = [
  "todays-sales",
  "total-orders",
  "active-branches",
  "low-stock",
];

const iconMap = {
  payments: Wallet,
  wallet: Wallet,
  "shopping-bag": ShoppingBag,
  users: Users,
  pill: Pill,
  "alert-triangle": AlertTriangle,
  "x-circle": XCircle,
  "building-2": Building2,
  clock: Clock,
  "calendar-x": CalendarX,
  "badge-check": BadgeCheck,
};

const KpiCard = ({ label, value, icon, trend, accent }) => {
  const Icon = iconMap[icon] ?? Wallet;
  const TrendIcon = trend?.direction === "up" ? TrendingUp : TrendingDown;
  const isAccentError = accent === "error";

  return (
    <div
      className="group rounded-xl border border-outline-variant bg-surface-container-lowest p-5 transition-all hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="mb-5 flex items-center justify-between">
        <span
          className={`flex h-10 w-10 items-center justify-center rounded-lg ${
            isAccentError
              ? "bg-error-container text-error"
              : accent
                ? "bg-primary text-on-primary"
                : "bg-primary-fixed text-primary"
          }`}
        >
          <Icon size={20} />
        </span>
        {trend && (
          <span
            className={`flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-bold ${
              trend.direction === "up"
                ? "bg-secondary-container text-on-secondary-fixed-variant"
                : "bg-error-container text-on-error-container"
            }`}
          >
            <TrendIcon size={12} />
            {trend.value}
          </span>
        )}
      </div>
      <h3 className="text-3xl font-bold tracking-tight text-on-background">{value}</h3>
      <p className="mt-1 text-sm font-medium text-on-surface-variant">{label}</p>
    </div>
  );
};

const KpiCards = () => {
  const featuredMetrics = featuredMetricIds.map((id) =>
    kpiSummary.find((metric) => metric.id === id),
  );

  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {featuredMetrics.map((metric) => (
        <KpiCard key={metric.id} {...metric} />
      ))}
    </section>
  );
};

export default KpiCards;
