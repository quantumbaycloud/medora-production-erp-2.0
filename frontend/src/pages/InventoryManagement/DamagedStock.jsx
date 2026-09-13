import { PackageX, DollarSign, AlertTriangle, Plus } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  damagedStockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  "Pending Action": "danger",
  "Under Review": "warning",
  "Resolved/Disposed": "success",
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
    key: "damagedQty",
    label: "Damaged Qty",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.damagedQty.toLocaleString()}
      </span>
    ),
  },
  {
    key: "unit",
    label: "Unit",
    render: (row) => <span className="text-on-surface-variant">{row.unit}</span>,
  },
  { key: "location", label: "Warehouse / Location" },
  { key: "reason", label: "Reason" },
  {
    key: "reportedBy",
    label: "Reported By",
    render: (row) => <span className="text-on-surface-variant">{row.reportedBy}</span>,
  },
  {
    key: "date",
    label: "Date",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.date}</span>,
  },
  {
    key: "status",
    label: "Status",
    align: "center",
    render: (row) => (
      <StatusBadge status={row.status} variant={statusVariantMap[row.status]} />
    ),
  },
];

const DamagedStock = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Damaged Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Track and manage damaged stock items for disposal.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Damaged Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={PackageX}
        />
        <StatCard
          title="Total Damaged Value"
          value="$24.5K"
          footerText="Estimated loss"
          footerIcon={DollarSign}
        />
        <StatCard
          title="Pending Disposal"
          value="12"
          footerText="Requires immediate action"
          footerIcon={AlertTriangle}
          footerClass="text-tertiary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Report Damage"
          actionIcon={Plus}
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={damagedStockItems} />

      <Pagination />
    </>
  );
};

export default DamagedStock;