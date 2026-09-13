# Medorax ERP — Frontend Structure

## Overview

This document describes the frontend folder structure of the Medorax ERP application.

- `pages/` — application-level pages/screens
- `components/` — reusable UI components belonging to a feature
- `data/` — static/mock data used by pages and components
- `layouts/` — common page layouts
- `routes/` — application routing
- `assets/` — images and other static assets

The purpose of this structure is to keep pages, reusable components, data, and layouts separated so that backend/API integration can be introduced without restructuring the frontend.

---

# src/

The main source directory of the application.

## App.jsx

**Location:**

`src/App.jsx`

**Purpose:**

Main application route configuration.

Currently defines routes for:

- Login
- Search
- Reports
- Import / Export
- Purchase Order
- Purchase Invoice

The dashboard-related pages are rendered through `DashboardLayout`.

---

## main.jsx

**Location:**

`src/main.jsx`

**Purpose:**

Application entry point.

It initializes the React application and renders the root application component.

---

## index.css

**Location:**

`src/index.css`

**Purpose:**

Global CSS styles used throughout the application.

---

# components/

Reusable UI components.

Components are grouped according to the feature they belong to.

---

## components/navbar/

### Navbar.jsx

**Location:**

`src/components/navbar/Navbar.jsx`

**Purpose:**

Top navigation/header component used inside the dashboard layout.

---

## components/sidebar/

Contains the dashboard sidebar and its smaller supporting components.

### Sidebar.jsx

Main sidebar component.

### SidebarBrand.jsx

Handles the branding/logo section of the sidebar.

### SidebarDropdown.jsx

Handles expandable/collapsible sidebar navigation groups.

### SidebarFooter.jsx

Handles the footer section of the sidebar.

### SidebarLink.jsx

Reusable individual navigation link.

### SidebarNav.jsx

Controls and renders the sidebar navigation items.

---

# components/reports/

Reusable components used by the Reports module.

### Shared.jsx

Contains shared UI elements used across report tabs, such as:

- statistical cards
- table elements
- pagination-related UI

### SalesTab.jsx

Sales report UI and sales-specific statistics/table.

### PurchaseTab.jsx

Purchase report UI and purchase-specific statistics/table.

### InventoryTab.jsx

Inventory report UI and inventory-specific statistics/table.

### GSTTab.jsx

GST-related reporting UI and statistics/table.

### ProfitTab.jsx

Profit reporting UI and statistics/table.

### CustomerTab.jsx

Customer reporting UI and customer statistics/table.

### SupplierTab.jsx

Supplier reporting UI and supplier statistics/table.

---

# components/purchases/

Reusable components used by the Purchases module.

### BatchEntryTab.jsx

UI for batch-related purchase entry information.

### CreditNotesTab.jsx

UI for managing/displaying credit note information.

### ExpiryEntryTab.jsx

UI for expiry-related purchase information.

### LineItemsTable.jsx

Reusable table for purchase line items.

### NotesAndSummary.jsx

Displays purchase notes and summary information.

### OrderDetailsSection.jsx

Displays and handles purchase order details.

### PurchaseReturnTab.jsx

UI for purchase return information.

### ReceiveGoodsTab.jsx

UI for receiving goods against purchase information.

### Shared.jsx

Shared purchase-related UI utilities/components.

---

# components/importExport/

Reusable components used by the Import/Export module.

### ImportPage.jsx

Handles the import interface.

### ExportPage.jsx

Handles the export interface.

### Shared.jsx

Shared UI components used by Import/Export functionality.

---

# data/

Contains static/mock data used by the frontend.

When backend/API integration is introduced, these files are potential locations to replace or supplement with API/service data.

---

## data/reports/

### data.js

Contains report configuration and report-related data such as:

- report tabs
- table configuration
- statistics configuration
- pagination-related constants

### mockData.js

Contains mock report records used while backend data is not connected.

---

## data/purchases/

### data.js

Contains purchase-related static/mock data, including data used by:

- purchase orders
- purchase invoices
- purchase returns
- receiving goods
- credit notes
- product/order options

---

## data/importExport/

### data.js

Contains Import/Export-related configuration and mock data.

This includes data required by the import and export interfaces.

---

## data/inventoryManagement/

Contains inventory-management data used by the inventory functionality.

---

## data/staffManagement/

Contains staff-management data.

### activityLogsData.js

Data used by the staff activity logs functionality.

### attendanceData.js

Data used by the staff attendance functionality.

---

# layouts/

Layouts provide common page structures shared by multiple pages.

---

## layouts/dashboard/

### DashboardLayout.jsx

**Location:**

`src/layouts/dashboard/DashboardLayout.jsx`

**Purpose:**

Main authenticated/dashboard layout.

It provides the common dashboard structure, including:

- Sidebar
- Navbar
- Main content area
- React Router outlet for rendering child pages

Pages that belong to the dashboard are rendered inside this layout.

---

## layouts/inventoryManagement/

Contains the layout used by Inventory Management functionality.

### InventoryLayout.jsx

Provides the common layout for inventory-management pages.

---

## layouts/staffManagement/

### StaffManagementLayout.jsx

Provides the common layout for staff-management pages.

---

## layouts/supplierManagement/

### SupplierManagemetnLayout.jsx

Provides the common layout for supplier-management functionality.

---

# pages/

Contains application-level pages/screens.

A page represents a complete route or major screen rather than a small reusable UI component.

---

## pages/Reports/

### ReportsPage.jsx

Main Reports page.

Combines the report tabs and shared reporting UI.

Available reporting areas include:

- Sales
- Purchases
- Inventory
- GST
- Profit
- Customers
- Suppliers

---

## pages/Purchases/

### PurchaseOrderPage.jsx

Purchase Order screen.

### PurchaseInvoicePage.jsx

Purchase Invoice screen.

---

## pages/ImportExport/

### ImportExportPage.jsx

Main Import/Export screen.

Provides access to the import and export functionality.

---

## pages/Search/

### SearchPage.jsx

Main search screen.

---

## pages/InventoryManagement/

Contains the Inventory Management screens.

Current pages include:

- AvailableStock.jsx
- BatchManagement.jsx
- ClosingStock.jsx
- CurrentStock.jsx
- DamagedStock.jsx
- ExpiredStock.jsx
- LowStockAlerts.jsx
- NearExpiry.jsx
- OpeningStock.jsx
- OverstockAlerts.jsx
- PhysicalVerification.jsx
- ReservedStock.jsx
- StockAdjustment.jsx
- StockLedger.jsx
- StockTransfer.jsx

Each file represents a separate Inventory Management screen.

---

## pages/StaffManagement/

Contains Staff Management screens.

### StaffInformation.jsx

Staff information screen.

### activityLogs/ActivityLogs.jsx

Activity logs screen.

### attendance/Attendance.jsx

Attendance screen.

### dashboard/Dashboard.jsx

Staff management dashboard.

### employee/Employee.jsx

Employee management screen.

### kiosk/Kiosk.jsx

Employee/staff kiosk screen.

---

## pages/SupplierManagement/

Contains Supplier Management screens.

### Dashboard.jsx

Supplier management dashboard.

### SupplierInformation.jsx

Supplier information screen.

### Suppliers.jsx

Supplier listing/management screen.

---

# routes/

Contains application routing configuration.

## routes/Router.jsx

Central routing configuration for the application.

Routes can be defined and organized here as the application expands.

---

# assets/

Contains static assets used by the application.

Examples include:

- logos
- images
- other frontend assets

---
