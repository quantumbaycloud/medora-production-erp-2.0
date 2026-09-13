import { createBrowserRouter, Navigate } from "react-router-dom";

import DashboardLayout from "../layouts/dashboard/DashboardLayout";
import SupplierLayout from "../layouts/supplierManagement/SupplierManagementLayout";
import StaffManagementLayout from "../layouts/staffManagement/StaffManagementLayout";
import InventoryLayout from "../layouts/inventoryManagement/InventoryLayout";
import BillingLayout from "../layouts/billing/BillingLayout";
import PharmacySettingsLayout from "../layouts/pharmacySettings/PharmacySettingsLayout";
import PurchaseLayout from "../layouts/purchases/PurchaseLayout";

import PharmacyDashboard from "../pages/PharmacySettings/Dashboard";
import PharmacySettingsPage from "../pages/PharmacySettings/Settings";
import PharmacyDirectory from "../pages/PharmacySettings/Directory";

import Login from "../pages/Authentication/Login";
import ForgotPassword from "../pages/Authentication/ForgotPassword";

import ChangePassword from "../pages/Authentication/ChangePassword";

import SearchPage from "../pages/Search/SearchPage";
import ReportsPage from "../pages/Reports/ReportsPage";
import ImportExportPage from "../pages/ImportExport/ImportExportPage";
import PurchaseOrderPage from "../pages/Purchases/PurchaseOrderPage";
import PurchaseInvoicePage from "../pages/Purchases/PurchaseInvoicePage";

import Dashboard from "../pages/SupplierManagement/Dashboard";
import Suppliers from "../pages/SupplierManagement/Suppliers";
import SupplierInformation from "../pages/SupplierManagement/SupplierInformation";

import StaffDashboard from "../pages/StaffManagement/dashboard/Dashboard";
import Employee from "../pages/StaffManagement/employee/Employee";
import StaffInformation from "../pages/StaffManagement/StaffInformation";
import Attendance from "../pages/StaffManagement/attendance/Attendance";
import ActivityLogs from "../pages/StaffManagement/activityLogs/ActivityLogs";
import Kiosk from "../pages/StaffManagement/kiosk/Kiosk";

import CurrentStock from "../pages/InventoryManagement/CurrentStock";
import OpeningStock from "../pages/InventoryManagement/OpeningStock";
import ClosingStock from "../pages/InventoryManagement/ClosingStock";
import AvailableStock from "../pages/InventoryManagement/AvailableStock";
import ReservedStock from "../pages/InventoryManagement/ReservedStock";
import BatchManagement from "../pages/InventoryManagement/BatchManagement";
import StockAdjustment from "../pages/InventoryManagement/StockAdjustment";
import StockTransfer from "../pages/InventoryManagement/StockTransfer";
import PhysicalVerification from "../pages/InventoryManagement/PhysicalVerification";
import DamagedStock from "../pages/InventoryManagement/DamagedStock";
import ExpiredStock from "../pages/InventoryManagement/ExpiredStock";
import NearExpiry from "../pages/InventoryManagement/NearExpiry";
import LowStockAlerts from "../pages/InventoryManagement/LowStockAlerts";
import OverstockAlerts from "../pages/InventoryManagement/OverstockAlerts";
import StockLedger from "../pages/InventoryManagement/StockLedger";

import BarcodeBilling from "../pages/Billing/BarcodeBilling";
import ManualBilling from "../pages/Billing/ManualBilling";
import QuickBilling from "../pages/Billing/QuickBilling";
import PrescriptionBilling from "../pages/Billing/PrescriptionBilling";
import SessionManagement from "../pages/SessionManagement/SessionManagement";
import LoginHistory from "../pages/LoginHistory/LoginHistory";
import LicenseManagement from "../pages/Licensing/LicenseManagement";
import ProfilePage from "../pages/Authentication/ProfilePage";
import ProtectedRoute from "./ProtectedRoute";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/forgot-password",
    element: <ForgotPassword />,
  },
  {
    path: "/change-password",
    element: <ChangePassword />,
  },
  {
    element: <ProtectedRoute requireLicense={false} />,
    children: [
      { path: "/sessions", element: <SessionManagement /> },
      { path: "/login-history", element: <LoginHistory /> },
      { path: "/license", element: <LicenseManagement /> },
      { path: "/profile", element: <ProfilePage /> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/",
        element: <DashboardLayout />,
        children: [
          { index: true, element: <PharmacyDashboard /> },
          {
            path: "suppliers",
            element: <SupplierLayout />,
            children: [
              { index: true, element: <Suppliers /> },
              { path: ":supplierId", element: <SupplierInformation /> },
            ],
          },
          {
            path: "search",
            element: <SearchPage />,
          },
          {
            path: "reports",
            element: <ReportsPage />,
          },
          {
            path: "import-export",
            element: <ImportExportPage />,
          },
          {
            path: "purchases",
            element: <PurchaseLayout />,
            children: [
              {
                path: "order",
                element: <PurchaseOrderPage />,
              },
              {
                path: "invoice",
                element: <PurchaseInvoicePage />,
              },
            ],
          },
          {
            path: "staff",
            element: <StaffManagementLayout />,
            children: [
              {
                index: true,
                element: <StaffDashboard />,
              },
              {
                path: "directory",
                element: <Employee />,
              },
              {
                path: "attendance",
                element: <Attendance />,
              },
              {
                path: "kiosk",
                element: <Kiosk />,
              },
              {
                path: "activity-logs",
                element: <ActivityLogs />,
              },
              {
                path: ":staffId",
                element: <StaffInformation />,
              },
            ],
          },
          {
            path: "billing",
            element: <BillingLayout />,
            children: [
              {
                index: true,
                element: <Navigate to="barcode" replace />,
              },
              {
                path: "barcode",
                element: <BarcodeBilling />,
              },
              {
                path: "manual",
                element: <ManualBilling />,
              },
              {
                path: "quick",
                element: <QuickBilling />,
              },
              {
                path: "prescription",
                element: <PrescriptionBilling />,
              },
            ],
          },
          {
            path: "pharmacy",
            element: <PharmacySettingsLayout />,
            children: [
              {
                index: true,
                element: <PharmacyDashboard />,
              },
              {
                path: "settings",
                element: <PharmacySettingsPage />,
              },
              {
                path: "directory",
                element: <PharmacyDirectory />,
              },
            ],
          },
          {
            path: "inventory",
            element: <InventoryLayout />,
            children: [
              {
                index: true,
                element: <CurrentStock />,
              },
              {
                path: "opening",
                element: <OpeningStock />,
              },
              {
                path: "closing",
                element: <ClosingStock />,
              },
              {
                path: "available",
                element: <AvailableStock />,
              },
              {
                path: "reserved",
                element: <ReservedStock />,
              },
              {
                path: "batches",
                element: <BatchManagement />,
              },
              {
                path: "adjustments",
                element: <StockAdjustment />,
              },
              {
                path: "transfers",
                element: <StockTransfer />,
              },
              {
                path: "verification",
                element: <PhysicalVerification />,
              },
              {
                path: "damaged",
                element: <DamagedStock />,
              },
              {
                path: "expired",
                element: <ExpiredStock />,
              },
              {
                path: "near-expiry",
                element: <NearExpiry />,
              },
              {
                path: "low-stock",
                element: <LowStockAlerts />,
              },
              {
                path: "overstock",
                element: <OverstockAlerts />,
              },
              {
                path: "stock-ledger",
                element: <StockLedger />,
              },
            ],
          },
        ],
      },
    ],
  },
]);

export default router;
