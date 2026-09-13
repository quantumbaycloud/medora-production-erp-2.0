import {
  Building,
  ClipboardList,
  ShoppingCart,
  UserPlus,
} from "lucide-react";
import { recentActivity } from "../../../data/pharmacySettings/pharmacySettingsData";

const activityIconMap = {
  "shopping-cart": ShoppingCart,
  "building-2": Building,
  pencil: ClipboardList,
  "log-in": UserPlus,
};

const toneClasses = {
  primary: "bg-primary/10 text-primary border-primary/20",
  secondary: "bg-primary-fixed text-on-primary-fixed-variant border-primary-fixed-dim",
  neutral: "bg-surface-container-high text-on-surface-variant border-outline-variant",
  muted: "bg-surface-container-low text-on-surface-variant border-outline-variant",
};

const ActivityFeed = () => (
  <section className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:p-6">
    <div className="mb-5 flex items-center justify-between">
      <div>
        <h4 className="text-lg font-bold text-on-background">Recent activity</h4>
        <p className="mt-1 text-xs text-on-surface-variant">Latest workspace updates</p>
      </div>
      <button type="button" className="text-xs font-bold text-primary hover:underline">
        View all
      </button>
    </div>
    <div className="space-y-5">
      {recentActivity.map(({ title, detail, meta, tone, icon }) => {
        const Icon = activityIconMap[icon] ?? ShoppingCart;

        return (
          <div key={meta} className="flex gap-3">
            <span
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border ${toneClasses[tone]}`}
            >
              <Icon size={16} />
            </span>
            <div>
              <p className="text-sm leading-5 text-on-background">
                <span className="font-bold">{title}</span> {detail}
              </p>
              <p className="text-[11px] font-medium text-on-surface-variant">{meta}</p>
            </div>
          </div>
        );
      })}
    </div>
  </section>
);

export default ActivityFeed;
