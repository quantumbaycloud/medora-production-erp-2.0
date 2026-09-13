import DashboardHeader from "../../components/supplierManagement/dashboard/DashboardHeader";
import KpiCards from "../../components/supplierManagement/dashboard/KpiCards";
import SupplierTable from "../../components/supplierManagement/dashboard/SupplierTable";

const Dashboard = () => {
  return (
    <>
      <DashboardHeader />
      <KpiCards />
      <SupplierTable />
    </>
  );
};

export default Dashboard;