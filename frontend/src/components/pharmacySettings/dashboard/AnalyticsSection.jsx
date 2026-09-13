import RevenueChart from "./RevenueChart";
import BranchPerformanceCard from "./BranchPerformanceCard";
import CategoryDistributionCard from "./CategoryDistributionCard";

const AnalyticsSection = () => (
  <div className="space-y-6">
    <RevenueChart />
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <BranchPerformanceCard />
      <CategoryDistributionCard />
    </div>
  </div>
);

export default AnalyticsSection;