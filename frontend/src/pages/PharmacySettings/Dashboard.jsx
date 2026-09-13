import DashboardHeader from "../../components/pharmacySettings/dashboard/DashboardHeader";
import KpiCards from "../../components/pharmacySettings/dashboard/KpiCards";
import RevenueChart from "../../components/pharmacySettings/dashboard/RevenueChart";
import RecentOrdersTable from "../../components/pharmacySettings/dashboard/RecentOrdersTable";
import LowStockPanel from "../../components/pharmacySettings/dashboard/LowStockPanel";
import ActivityFeed from "../../components/pharmacySettings/dashboard/ActivityFeed";

const Dashboard = () => {
  return (
    <div className="space-y-8">
      <DashboardHeader />
      <KpiCards />

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <RevenueChart />
        </div>
        <LowStockPanel />
      </div>

      <div className="grid items-start gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <RecentOrdersTable />
        </div>
        <ActivityFeed />
      </div>
    </div>
  );
};

export default Dashboard;
