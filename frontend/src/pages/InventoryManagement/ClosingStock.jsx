import { useState } from "react";
import { TrendingUp, CheckCircle2, Info } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import EntryModal from "../../components/inventoryManagement/common/EntryModal";
import { closingStockFields } from "../../components/inventoryManagement/common/entryModalConfigs";
import {
  closingStockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

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
    key: "closingQty",
    label: "Closing Stock Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.closingQty.toLocaleString()}
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
    key: "remarks",
    label: "Remarks / Notes",
    align: "center",
    render: (row) => (
      <span className="text-xs text-on-surface-variant">{row.remarks}</span>
    ),
  },
  {
    key: "periodEndDate",
    label: "Period End Date",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.periodEndDate}</span>,
  },
];

const ClosingStock = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Closing Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Review stock quantities at the end of the reporting period.
        </p>
      </div>


      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Closing Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={TrendingUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Total Closing Stock Value"
          value="$2.4M"
          footerText="Inventory healthy"
          footerIcon={CheckCircle2}
          footerClass="text-secondary"
        />
        <StatCard
          title="Period End Date"
          value="Oct 31, 2023"
          footerText="No action required"
          footerIcon={Info}
          footerClass="text-secondary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Add Closing Stock"
          onAction={() => setIsModalOpen(true)}
        />
      </div>

      <DataTable columns={columns} rows={closingStockItems} />

      <Pagination />

      <EntryModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Closing Stock"
        submitLabel="Add Closing Stock"
        fields={closingStockFields}
        onSubmit={() => {}}
      />
    </>
  );
};

export default ClosingStock;
