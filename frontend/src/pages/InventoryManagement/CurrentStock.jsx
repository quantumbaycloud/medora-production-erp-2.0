import { useState } from "react";
import { ArrowUp, TrendingUp, AlertTriangle, MoreVertical } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import EntryModal from "../../components/inventoryManagement/common/EntryModal";
import { addStockFields } from "../../components/inventoryManagement/common/entryModalConfigs";
import {
  currentStockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  "In Stock": "success",
  "Low Stock": "warning",
  "Out of Stock": "danger",
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
    label: "SKU / Code",
    render: (row) => (
      <span className="text-xs text-on-surface-variant">{row.sku}</span>
    ),
  },
  { key: "category", label: "Category" },
  {
    key: "quantity",
    label: "Qty",
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
  { key: "location", label: "Location" },
  {
    key: "status",
    label: "Status",
    align: "center",
    render: (row) => (
      <StatusBadge status={row.status} variant={statusVariantMap[row.status]} />
    ),
  },
  {
    key: "lastUpdated",
    label: "Last Updated",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.lastUpdated}</span>,
  },
  {
    key: "actions",
    label: "Actions",
    align: "center",
    render: () => (
      <button
        type="button"
        className="rounded-lg p-1.5 text-outline transition hover:bg-surface-container hover:text-primary"
        aria-label="More actions"
      >
        <MoreVertical size={18} />
      </button>
    ),
  },
];

const CurrentStock = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Current Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Monitor real-time inventory levels across all warehouses.
        </p>
      </div>


      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={ArrowUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Total Stock Value"
          value="$2.4M"
          footerText="Inventory healthy"
          footerIcon={TrendingUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Low Stock Items"
          value="342"
          footerText="Action required on 12"
          footerIcon={AlertTriangle}
          footerClass="text-tertiary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Add Stock"
          onAction={() => setIsModalOpen(true)}
        />
      </div>

      <DataTable columns={columns} rows={currentStockItems} />

      <Pagination />

      <EntryModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add New Stock"
        submitLabel="Add Stock"
        fields={addStockFields}
        onSubmit={() => {}}
      />
    </>
  );
};

export default CurrentStock;
