import QuickActionsPanel from "./QuickActionsPanel";
import LowStockPanel from "./LowStockPanel";
import ActivityFeed from "./ActivityFeed";

const SidePanels = () => (
  <div className="space-y-6">
    <QuickActionsPanel />
    <LowStockPanel />
    <ActivityFeed />
  </div>
);

export default SidePanels;