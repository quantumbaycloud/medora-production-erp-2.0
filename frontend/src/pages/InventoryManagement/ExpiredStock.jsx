import { CalendarX, DollarSign, Trash2 } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  expiredStockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  "Pending Action": "danger",
  "Under Review": "warning",
  Disposed: "success",
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
    key: "expiredQty",
    label: "Expired Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.expiredQty.toLocaleString()}
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

const ExpiredStock = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Expired Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Track and manage expired stock items for disposal.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Expired Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={CalendarX}
          footerClass="text-error"
        />
        <StatCard
          title="Total Expired Value"
          value="$32.8K"
          footerText="6.3% vs last month"
          footerIcon={DollarSign}
          footerClass="text-error"
        />
        <StatCard
          title="Pending Disposal"
          value="24"
          footerText="Requires immediate attention"
          footerIcon={Trash2}
          footerClass="text-secondary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Dispose Stock"
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={expiredStockItems} />

      <Pagination />
    </>
  );
};

export default ExpiredStock;