import {Routes, Route } from "react-router-dom";
import Login from "@/pages/Authentication/Login";
import SearchPage from "./pages/Search/SearchPage";
import DashboardLayout from "./layouts/dashboard/DashboardLayout";
import PurchaseOrderPage from "./pages/Purchases/PurchaseOrderPage";
import PurchaseInvoicePage from "./pages/Purchases/PurchaseInvoicePage";
import ImportExportPage from "./pages/ImportExport/ImportExportPage";
import ReportsPage from "./pages/Reports/ReportsPage";
import ChangePassword from "./pages/Authentication/ChangePassword";
import SessionManagement from "./pages/SessionManagement/SessionManagement";
import LoginHistory from "./pages/LoginHistory/LoginHistory";
import Suppliers from "./pages/SupplierManagement/Suppliers";
import MasterData from "./pages/PharmacySettings/MasterData";


function App() {
  return (
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/change-password" element={<ChangePassword/>} />
        <Route path="/sessions" element={<SessionManagement/>} />
        <Route path="/login-history" element={<LoginHistory/>} />

        <Route element={<DashboardLayout />}>
          <Route path="/search" element={<SearchPage/>} />
          <Route path="/suppliers" element={<Suppliers/>} />
          <Route path="/pharmacy/settings" element={<MasterData/>} />
          <Route path="/reports" element={<ReportsPage/>} />
          <Route path="/import-export" element={<ImportExportPage/>} />
          <Route path="/purchases/order" element={<PurchaseOrderPage/>} />
          <Route path="/purchases/invoice" element={<PurchaseInvoicePage/>} />
        </Route>
      </Routes>
  );
}

export default App;