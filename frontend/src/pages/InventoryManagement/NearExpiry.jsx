import { AlertTriangle, DollarSign, Clock } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  nearExpiryItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  "Urgent/Under 1 month": "danger",
  "Near Expiry/1-3 months": "warning",
  "Safe/6+ months": "success",
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
  { key: "batchNumber", label: "Batch Number" },
  {
    key: "expiryDate",
    label: "Expiry Date",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.expiryDate}</span>,
  },
  {
    key: "timeRemaining",
    label: "Time Remaining",
    render: (row) => <span className="text-on-surface-variant">{row.timeRemaining}</span>,
  },
  {
    key: "quantity",
    label: "Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.quantity.toLocaleString()}
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

const NearExpiry = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Near Expiry Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Monitor stock approaching expiry to minimize waste.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Items Near Expiry"
          value="14,285"
          footerText="Items requiring attention"
          footerIcon={AlertTriangle}
          footerClass="text-tertiary"
        />
        <StatCard
          title="Expiring in 30 Days"
          value="$32.8K"
          footerText="High priority disposal risk"
          footerIcon={DollarSign}
          footerClass="text-error"
        />
        <StatCard
          title="Total Value at Risk"
          value="24"
          footerText="Estimated loss if not utilized"
          footerIcon={Clock}
          footerClass="text-tertiary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Export"
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={nearExpiryItems} />

      <Pagination />
    </>
  );
};

export default NearExpiry;