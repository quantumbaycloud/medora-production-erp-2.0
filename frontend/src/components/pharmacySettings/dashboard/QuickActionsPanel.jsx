import {
  Boxes,
  Building,
  ClipboardList,
  FileBarChart2,
  PackagePlus,
  UserPlus,
} from "lucide-react";
import { quickActions } from "../../../data/pharmacySettings/pharmacySettingsData";

const actionIconMap = {
  "package-plus": PackagePlus,
  building: Building,
  "user-plus": UserPlus,
  "clipboard-list": ClipboardList,
  "file-bar-chart": FileBarChart2,
  boxes: Boxes,
};

const QuickActionsPanel = () => (
  <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
    <h4 className="mb-4 text-xl font-semibold text-on-background">Quick Actions</h4>
    <div className="grid grid-cols-2 gap-3">
      {quickActions.map(({ id, label, icon }) => {
        const Icon = actionIconMap[icon] ?? Boxes;

        return (
          <button
            key={id}
            type="button"
            className="group flex flex-col items-center justify-center rounded-xl border border-outline-variant bg-surface-container-low p-4 transition-all hover:border-primary hover:text-primary"
          >
            <Icon
              size={22}
              className="mb-2 text-primary transition-transform group-hover:scale-110"
            />
            <span className="text-[11px] font-bold">{label}</span>
          </button>
        );
      })}
    </div>
  </div>
);

export default QuickActionsPanel;