import {
  AlertTriangle,
  ArrowLeftRight,
  BarChart3,
  Boxes,
  CalendarDays,
  CalendarX,
  ClipboardCheck,
  Clock,
  FileText,
  Keyboard,
  Layers,
  LayoutDashboard,
  LogIn,
  Package,
  PackageCheck,
  PackageX,
  Pill,
  Receipt,
  ScanBarcode,
  ScrollText,
  Search,
  Settings2,
  ShoppingCart,
  TrendingDown,
  UserCheck,
  Users,
  Zap,
} from "lucide-react";

export const primaryNavigation = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/suppliers", label: "Suppliers", icon: Users },
  { to: "/inventory", label: "Inventory", icon: Package },
  {
    to: "/purchases/order",
    label: "Purchases",
    icon: ShoppingCart,
    activePrefix: "/purchases",
  },
  { to: "/billing", label: "Billing", icon: Receipt },
  { to: "/staff", label: "Staff", icon: UserCheck },
  { to: "/pharmacy", label: "Pharmacy", icon: Pill },
];

export const utilityNavigation = [
  { to: "/search", label: "Search", icon: Search },
  { to: "/reports", label: "Reports", icon: BarChart3 },
  { to: "/import-export", label: "Import / Export", icon: ArrowLeftRight },
];

export const moduleNavigation = {
  supplier: {
    title: "Supplier Management",
    description: "Manage supplier records and performance",
    items: [
      { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
      { to: "/suppliers", label: "Suppliers", icon: Users },
    ],
  },
  staff: {
    title: "Staff Management",
    description: "Manage employees, attendance, and access activity",
    items: [
      { to: "/staff", label: "Dashboard", icon: LayoutDashboard, end: true },
      { to: "/staff/directory", label: "Employees", icon: UserCheck },
      { to: "/staff/attendance", label: "Attendance", icon: CalendarDays },
      { to: "/staff/kiosk", label: "Check In / Out", icon: LogIn },
      { to: "/staff/activity-logs", label: "Activity Logs", icon: ScrollText },
    ],
  },
  inventory: {
    title: "Inventory Management",
    description: "Track stock, batches, movements, and alerts",
    items: [
      { to: "/inventory", label: "Current Stock", icon: Package, end: true },
      { to: "/inventory/opening", label: "Opening Stock", icon: Boxes },
      { to: "/inventory/closing", label: "Closing Stock", icon: Layers },
      { to: "/inventory/available", label: "Available Stock", icon: PackageCheck },
      { to: "/inventory/reserved", label: "Reserved Stock", icon: PackageX },
      { to: "/inventory/batches", label: "Batches", icon: Boxes },
      { to: "/inventory/adjustments", label: "Adjustments", icon: ArrowLeftRight },
      { to: "/inventory/transfers", label: "Transfers", icon: ArrowLeftRight },
      { to: "/inventory/verification", label: "Verification", icon: ClipboardCheck },
      { to: "/inventory/damaged", label: "Damaged", icon: PackageX },
      { to: "/inventory/expired", label: "Expired", icon: CalendarX },
      { to: "/inventory/near-expiry", label: "Near Expiry", icon: AlertTriangle },
      { to: "/inventory/low-stock", label: "Low Stock", icon: TrendingDown },
      { to: "/inventory/overstock", label: "Overstock", icon: PackageCheck },
      { to: "/inventory/stock-ledger", label: "Stock Ledger", icon: Clock },
    ],
  },
  billing: {
    title: "Billing (POS)",
    description: "Create bills with the workflow that suits the sale",
    items: [
      { to: "/billing/barcode", label: "Barcode Billing", icon: ScanBarcode },
      { to: "/billing/manual", label: "Manual Billing", icon: Keyboard },
      { to: "/billing/quick", label: "Quick Billing", icon: Zap },
      { to: "/billing/prescription", label: "Prescription Billing", icon: FileText },
    ],
  },
  pharmacy: {
    title: "Pharmacy Management",
    description: "Manage pharmacy details, branches, and configuration",
    items: [
      { to: "/pharmacy", label: "Dashboard", icon: LayoutDashboard, end: true },
      { to: "/pharmacy/settings", label: "Settings", icon: Settings2 },
      { to: "/pharmacy/directory", label: "My Pharmacies", icon: Pill },
    ],
  },
  purchases: {
    title: "Purchase Management",
    description: "Create purchase orders and record supplier invoices",
    items: [
      { to: "/purchases/order", label: "Purchase Order", icon: ShoppingCart },
      { to: "/purchases/invoice", label: "Purchase Invoice", icon: FileText },
    ],
  },
};
