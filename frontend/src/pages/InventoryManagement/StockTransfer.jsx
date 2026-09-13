import { ArrowUp, AlertTriangle, Plus } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  stockTransferItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  Completed: "success",
  "In Transit": "warning",
  Cancelled: "danger",
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
    key: "transferQty",
    label: "Transfer Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.transferQty.toLocaleString()}
      </span>
    ),
  },
  { key: "fromWarehouse", label: "From Warehouse" },
  { key: "toWarehouse", label: "To Warehouse" },
  {
    key: "transferredBy",
    label: "Transferred By",
    render: (row) => <span className="text-on-surface-variant">{row.transferredBy}</span>,
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

const StockTransfer = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Stock Transfer
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Manage stock transfers between warehouses and facilities.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Transfers Today"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={ArrowUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Pending Transfers"
          value="12"
          footerText="Requires immediate attention"
          footerIcon={AlertTriangle}
          footerClass="text-tertiary"
        />
        <StatCard
          title="Total Quantity Transferred"
          value="342"
          subtitle="Net transfers for the period"
          footerIcon={AlertTriangle}
          footerText="Warning"
          footerClass="text-tertiary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="New Transfer"
          actionIcon={Plus}
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={stockTransferItems} />

      <Pagination />
    </>
  );
};

export default StockTransfer;