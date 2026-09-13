import { PackageCheck, AlertTriangle, DollarSign, ArrowLeftRight } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  overstockItems,
  categories,
  warehouses,
} from "../../data/inventoryManagement/inventoryData";

const statusVariantMap = {
  Overstocked: "warning",
  "Severely Overstocked": "danger",
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
    key: "idealMaxThreshold",
    label: "Ideal Max Threshold",
    align: "right",
    render: (row) => (
      <span className="text-on-surface-variant">
        {row.idealMaxThreshold.toLocaleString()}
      </span>
    ),
  },
  {
    key: "excessQty",
    label: "Excess Quantity",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-tertiary-fixed-variant">
        +{row.excessQty.toLocaleString()}
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

const OverstockAlerts = () => {
  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Overstock Alerts
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Identify items exceeding ideal maximum stock thresholds.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Overstocked Items"
          value="148"
          footerText="Items exceeding ideal max thresholds"
          footerIcon={PackageCheck}
          footerClass="text-tertiary"
        />
        <StatCard
          title="Severely Overstocked"
          value="32"
          footerText="Critical excess requiring redistribution"
          footerIcon={AlertTriangle}
          footerClass="text-error"
        />
        <StatCard
          title="Excess Stock Value"
          value="$245k"
          footerText="Total capital tied in surplus inventory"
          footerIcon={DollarSign}
          footerClass="text-tertiary"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="Redistribute"
          actionIcon={ArrowLeftRight}
          onAction={() => {}}
        />
      </div>

      <DataTable columns={columns} rows={overstockItems} />

      <Pagination />
    </>
  );
};

export default OverstockAlerts;
