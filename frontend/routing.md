# Medorax ERP — Routing Map

## Overview

All application routes are defined in **`src/routes/Router.jsx`** using `createBrowserRouter` (react-router-dom v6+), wired via `RouterProvider` in `src/main.jsx`.

The legacy component-router configuration in `src/App.jsx` (`Routes`/`Route`) is **kept for reference only** — its routes have been migrated into the data router and are now mounted.

Routes are grouped under **six top-level layouts / screens**:

| Module | Base Path | Layout |
| --- | --- | --- |
| Authentication (Login) | `/login` | standalone |
| Legacy dashboard pages | `/` | `DashboardLayout` |
| Supplier Management | `/` | `SupplierManagemetnLayout` |
| Staff Management | `/staff` | `StaffManagementLayout` |
| Inventory Management | `/inventory` | `InventoryLayout` |
| Billing | `/billing` | `BillingLayout` |

> **Note:** Two route groups share the base path `/` (`DashboardLayout` and `SupplierLayout`). The `SupplierLayout` route is declared first so `/` resolves to the Supplier dashboard index. The `DashboardLayout` group only matches its explicit child paths (`/search`, `/reports`, `/import-export`, `/purchases/*`).

---

## 1. Authentication — `/login`

Standalone route (no layout wrapper).

| Path | Component | File |
| --- | --- | --- |
| `/login` | `Login` | `src/pages/Authentication/Login.jsx` |
| `/forgot-password` | `ForgotPassword` | `src/pages/Authentication/ForgotPassword.jsx` |
| `/verify-email` | `VerifyEmail` | `src/pages/Authentication/VerifyEmail.jsx` |
| `/change-password` | `ChangePassword` | `src/pages/Authentication/ChangePassword.jsx` |
| `/login-history` | `LoginHistory` | `src/pages/LoginHistory/LoginHistory.jsx` |
| `/sessions` | `SessionManagement` | `src/pages/SessionManagement/SessionManagement.jsx` |

Renders the self-contained `LoginForm` component (`src/components/authentication/login/LoginForm/LoginForm.jsx`).

---

## 2. Legacy Dashboard — `/`

Layout: `src/layouts/dashboard/DashboardLayout.jsx` (composes `Navbar` + `Sidebar`)

| Path | Component | File |
| --- | --- | --- |
| `/search` | `SearchPage` | `src/pages/Search/SearchPage.jsx` |
| `/reports` | `ReportsPage` | `src/pages/Reports/ReportsPage.jsx` |
| `/import-export` | `ImportExportPage` | `src/pages/ImportExport/ImportExportPage.jsx` |
| `/purchases/order` | `PurchaseOrderPage` | `src/pages/Purchases/PurchaseOrderPage.jsx` |
| `/purchases/invoice` | `PurchaseInvoicePage` | `src/pages/Purchases/PurchaseInvoicePage.jsx` |

No index route; only the explicit paths above are matched.

---

## 3. Supplier Management — `/`

Layout: `src/layouts/supplierManagement/SupplierManagemetnLayout.jsx`

| Path | Component | File |
| --- | --- | --- |
| `/` | `Dashboard` | `src/pages/SupplierManagement/Dashboard.jsx` |
| `/suppliers` | `Suppliers` | `src/pages/SupplierManagement/Suppliers.jsx` |
| `/suppliers/:supplierId` | `SupplierInformation` | `src/pages/SupplierManagement/SupplierInformation.jsx` |

**Index route:** `/`

---

## 4. Staff Management — `/staff`

Layout: `src/layouts/staffManagement/StaffManagementLayout.jsx`

| Path | Component | File |
| --- | --- | --- |
| `/staff` | `StaffDashboard` | `src/pages/StaffManagement/dashboard/Dashboard.jsx` |
| `/staff/directory` | `Employee` | `src/pages/StaffManagement/employee/Employee.jsx` |
| `/staff/attendance` | `Attendance` | `src/pages/StaffManagement/attendance/Attendance.jsx` |
| `/staff/kiosk` | `Kiosk` | `src/pages/StaffManagement/kiosk/Kiosk.jsx` |
| `/staff/activity-logs` | `ActivityLogs` | `src/pages/StaffManagement/activityLogs/ActivityLogs.jsx` |
| `/staff/:staffId` | `StaffInformation` | `src/pages/StaffManagement/StaffInformation.jsx` |

**Index route:** `/staff`

> **Note:** `/staff/:staffId` is dynamic. React Router ranks static segments (`directory`, `attendance`, `kiosk`, `activity-logs`) above the dynamic `:staffId`, so no conflict occurs.

---

## 5. Inventory Management — `/inventory`

Layout: `src/layouts/inventoryManagement/InventoryLayout.jsx`

| Path | Component | File |
| --- | --- | --- |
| `/inventory` | `CurrentStock` | `src/pages/InventoryManagement/CurrentStock.jsx` |
| `/inventory/opening` | `OpeningStock` | `src/pages/InventoryManagement/OpeningStock.jsx` |
| `/inventory/closing` | `ClosingStock` | `src/pages/InventoryManagement/ClosingStock.jsx` |
| `/inventory/available` | `AvailableStock` | `src/pages/InventoryManagement/AvailableStock.jsx` |
| `/inventory/reserved` | `ReservedStock` | `src/pages/InventoryManagement/ReservedStock.jsx` |
| `/inventory/batches` | `BatchManagement` | `src/pages/InventoryManagement/BatchManagement.jsx` |
| `/inventory/adjustments` | `StockAdjustment` | `src/pages/InventoryManagement/StockAdjustment.jsx` |
| `/inventory/transfers` | `StockTransfer` | `src/pages/InventoryManagement/StockTransfer.jsx` |
| `/inventory/verification` | `PhysicalVerification` | `src/pages/InventoryManagement/PhysicalVerification.jsx` |
| `/inventory/damaged` | `DamagedStock` | `src/pages/InventoryManagement/DamagedStock.jsx` |
| `/inventory/expired` | `ExpiredStock` | `src/pages/InventoryManagement/ExpiredStock.jsx` |
| `/inventory/near-expiry` | `NearExpiry` | `src/pages/InventoryManagement/NearExpiry.jsx` |
| `/inventory/low-stock` | `LowStockAlerts` | `src/pages/InventoryManagement/LowStockAlerts.jsx` |
| `/inventory/overstock` | `OverstockAlerts` | `src/pages/InventoryManagement/OverstockAlerts.jsx` |
| `/inventory/stock-ledger` | `StockLedger` | `src/pages/InventoryManagement/StockLedger.jsx` |

**Index route:** `/inventory` → `CurrentStock`

---

## 6. Billing — `/billing`

Layout: `src/layouts/billing/BillingLayout.jsx`

| Path | Component | File |
| --- | --- | --- |
| `/billing` | `BarcodeBilling` | `src/pages/Billing/BarcodeBilling.jsx` |
| `/billing/barcode` | `BarcodeBilling` | `src/pages/Billing/BarcodeBilling.jsx` |
| `/billing/manual` | `ManualBilling` | `src/pages/Billing/ManualBilling.jsx` |
| `/billing/quick` | `QuickBilling` | `src/pages/Billing/QuickBilling.jsx` |
| `/billing/prescription` | `PrescriptionBilling` | `src/pages/Billing/PrescriptionBilling.jsx` |

**Index route:** `/billing` → `BarcodeBilling`

> **Note:** `/billing` and `/billing/barcode` both render `BarcodeBilling`. The index route is the default landing; the explicit `barcode` path allows direct navigation.

---

## Entry Point Wiring (`src/main.jsx`)

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import "./index.css";
import router from "./routes/Router";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
```

---

## Route Segment Conventions

| Segment | Meaning |
| --- | --- |
| `:supplierId` | Dynamic supplier identifier (Supplier Management) |
| `:staffId` | Dynamic staff/employee identifier (Staff Management) |

---

## Summary

- **42 route definitions**, all mounted in `src/routes/Router.jsx` via `RouterProvider`.
- Includes the migrated legacy routes: `/login`, `/search`, `/reports`, `/import-export`, `/purchases/order`, `/purchases/invoice`.
- Routing is fully centralized in `src/routes/Router.jsx`; `src/App.jsx` is retained for reference only.