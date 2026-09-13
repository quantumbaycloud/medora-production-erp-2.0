import { useState } from "react";
import { ArrowUp, TrendingUp, Info } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import EntryModal from "../../components/inventoryManagement/common/EntryModal";
import { openingStockFields } from "../../components/inventoryManagement/common/entryModalConfigs";
import {
  openingStockItems,
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
    key: "openingQty",
    label: "Opening Qty",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.openingQty.toLocaleString()}
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
    key: "periodStartDate",
    label: "Period Start Date",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.periodStartDate}</span>,
  },
];

const OpeningStock = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Opening Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Review stock quantities at the start of the reporting period.
        </p>
      </div>


      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Opening Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={ArrowUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Total Opening Stock Value"
          value="$2.4M"
          footerText="Inventory healthy"
          footerIcon={TrendingUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Period Start Date"
          value="Oct 01, 2023"
          footerText="Opening balance period"
          footerIcon={Info}
          footerClass="text-secondary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Add Opening Stock"
          onAction={() => setIsModalOpen(true)}
        />
      </div>

      <DataTable columns={columns} rows={openingStockItems} />

      <Pagination />

      <EntryModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Opening Stock"
        submitLabel="Add Opening Stock"
        fields={openingStockFields}
        onSubmit={() => {}}
      />
    </>
  );
};

export default OpeningStock;
