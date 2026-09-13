import { TrendingDown, AlertTriangle, ShoppingCart, RefreshCw } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  lowStockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  Low: "warning",
  Critical: "danger",
};

const columns = [
  {
    key: "name",
    label: "Item Name",
    render: (row) => (
      <span className="font-medium text-on-background">{row.name}</span>
    ),
  },
  {
    key: "sku",
    label: "SKU / Item Code",
    render: (row) => (
      <span className="text-xs text-on-surface-variant">{row.sku}</span>
    ),
  },
  {
    key: "currentQty",
    label: "Current Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.currentQty.toLocaleString()}
      </span>
    ),
  },
  {
    key: "reorderThreshold",
    label: "Reorder Threshold",
    align: "right",
    render: (row) => (
      <span className="text-on-surface-variant">{row.reorderThreshold.toLocaleString()}</span>
    ),
  },
  {
    key: "shortageAmount",
    label: "Shortage Amount",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-error">
        {row.shortageAmount.toLocaleString()}
      </span>
    ),
  },
  {
    key: "unit",
    label: "Unit",
    render: (row) => <span className="text-on-surface-variant">{row.unit}</span>,
  },
  { key: "location", label: "Warehouse / Location" },
  {
    key: "status",
    label: "Status",
    align: "center",
    render: (row) => (
      <StatusBadge status={row.status} variant={statusVariantMap[row.status]} />
    ),
  },
];

const LowStockAlerts = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Low Stock Alerts
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Identify items below recommended stock thresholds.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Items Low on Stock"
          value="148"
          footerText="Items below recommended threshold"
          footerIcon={TrendingDown}
          footerClass="text-tertiary"
        />
        <StatCard
          title="Critical Items"
          value="32"
          footerText="Requires immediate reordering"
          footerIcon={AlertTriangle}
          footerClass="text-error"
        />
        <StatCard
          title="Items Pending Reorder"
          value="24"
          footerText="Currently in procurement queue"
          footerIcon={ShoppingCart}
          footerClass="text-primary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Reorder Now"
          actionIcon={RefreshCw}
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={lowStockItems} />

      <Pagination />
    </>
  );
};

export default LowStockAlerts;