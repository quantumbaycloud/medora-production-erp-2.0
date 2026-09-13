import { useState } from "react";
import { ArrowUp, TrendingUp, Info } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import EntryModal from "../../components/inventoryManagement/common/EntryModal";
import { reservedStockFields } from "../../components/inventoryManagement/common/entryModalConfigs";
import {
  reservedStockItems,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  Confirmed: "success",
  Pending: "warning",
  Expired: "danger",
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
  { key: "category", label: "Category" },
  {
    key: "reservedQty",
    label: "Reserved Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.reservedQty.toLocaleString()}
      </span>
    ),
  },
  { key: "reservedFor", label: "Reserved For" },
  {
    key: "unit",
    label: "Unit",
    render: (row) => <span className="text-on-surface-variant">{row.unit}</span>,
  },
  { key: "location", label: "Warehouse / Location" },
  {
    key: "reservationDate",
    label: "Reservation Date",
    render: (row) => <span className="text-xs text-on-surface-variant">{row.reservationDate}</span>,
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

const ReservedStock = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Reserved Stock
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Track stock reserved for pending orders and commitments.
        </p>
      </div>


      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Reserved Items"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={ArrowUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Total Reserved Stock Value"
          value="$2.4M"
          footerText="Inventory healthy"
          footerIcon={TrendingUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Pending Orders/Reservations"
          value="Oct 31, 2023"
          footerText="No action required"
          footerIcon={Info}
          footerClass="text-secondary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          warehouses={warehouses}
          actionLabel="Add Reservation"
          onAction={() => setIsModalOpen(true)}
        />
      </div>

      <DataTable columns={columns} rows={reservedStockItems} />

      <Pagination />

      <EntryModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Reservation"
        submitLabel="Add Reservation"
        fields={reservedStockFields}
        onSubmit={() => {}}
      />
    </>
  );
};

export default ReservedStock;
