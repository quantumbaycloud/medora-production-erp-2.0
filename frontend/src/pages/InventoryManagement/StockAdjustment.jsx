import { useMemo, useState } from "react";
import { ArrowUp, AlertTriangle, Plus, X } from "lucide-react";

import StatCard from "../../components/inventoryManagement/common/StatCard";
import FilterBar from "../../components/inventoryManagement/common/FilterBar";
import DataTable from "../../components/inventoryManagement/common/DataTable";
import Pagination from "../../components/inventoryManagement/common/Pagination";
import StatusBadge from "../../components/inventoryManagement/common/StatusBadge";
import {
  stockAdjustmentItems,
  categories,
  warehouses,
  currentStockItems,
} from "../../data/inventoryManagement/inventoryData";
import erpApi from "../../services/erpApi";

const statusVariantMap = {
  Approved: "success",
  Pending: "warning",
  Rejected: "danger",
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
    key: "currentStock",
    label: "Current Stock",
    align: "right",
    render: (row) => (
      <span className="font-semibold text-on-background">
        {row.currentStock.toLocaleString()}
      </span>
    ),
  },
  {
    key: "adjQty",
    label: "Adj. Qty (+/-)",
    align: "right",
    render: (row) => (
      <span
        className={`font-semibold ${
          row.adjQty < 0 ? "text-error" : "text-secondary"
        }`}
      >
        {row.adjQty > 0 ? `+${row.adjQty}` : row.adjQty}
      </span>
    ),
  },
  {
    key: "adjustedBy",
    label: "Adjusted By",
    render: (row) => <span className="text-on-surface-variant">{row.adjustedBy}</span>,
  },
  { key: "reason", label: "Reason" },
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

const StockAdjustment = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [medicineId, setMedicineId] = useState(currentStockItems[0]?.id || "");
  const [batchNumber, setBatchNumber] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [type, setType] = useState("decrease");
  const [reason, setReason] = useState("Damaged");
  const [notes, setNotes] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const selectedMedicine = useMemo(() => currentStockItems.find((item) => item.id === medicineId), [medicineId]);

  return (
    <>
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Stock Adjustment
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Manage stock quantity adjustments and approvals.
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-3">
        <StatCard
          title="Total Adjustments Today"
          value="14,285"
          footerText="2.4% vs last month"
          footerIcon={ArrowUp}
          footerClass="text-secondary"
        />
        <StatCard
          title="Pending Approvals"
          value="12"
          footerText="Requires immediate attention"
          footerIcon={AlertTriangle}
          footerClass="text-tertiary"
        />
        <StatCard
          title="Total Quantity Adjusted"
          value="342"
          subtitle="Net adjustment for the period"
          footerIcon={AlertTriangle}
          footerText="Warning"
          footerClass="text-error"
        />
      </div>

      <div className="mb-6">
        <FilterBar
          searchPlaceholder="Search by Name, SKU, or Code..."
          categories={categories}
          warehouses={warehouses}
          actionLabel="New Adjustment"
          actionIcon={Plus}
          onAction={() => setIsModalOpen(true)}
        />
      </div>

      <DataTable columns={columns} rows={stockAdjustmentItems} />

      <Pagination />

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-inverse-surface/50 p-4 backdrop-blur-sm">
          <div className="w-full max-w-lg overflow-hidden rounded-2xl bg-surface-container-lowest shadow-xl">
            <div className="flex items-center justify-between border-b border-outline-variant px-6 py-4">
              <h2 className="text-lg font-bold text-on-background">
                New Stock Adjustment
              </h2>
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="rounded-lg p-1 text-outline transition hover:bg-surface-container hover:text-on-surface-variant"
                aria-label="Close"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4 p-6">
              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">
                  Item Name / SKU
                </label>
                <select value={medicineId} onChange={(e) => setMedicineId(e.target.value)} className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed">
                  {currentStockItems.map((item) => <option key={item.id} value={item.id}>{item.name} - {item.sku}</option>)}
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">Batch Number</label>
                <input value={batchNumber} onChange={(e) => setBatchNumber(e.target.value)} placeholder="Enter exact batch number" className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm" required />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">
                  Current Stock Quantity
                </label>
                <input
                  type="text"
                  readOnly
                  value={selectedMedicine?.quantity?.toLocaleString?.() || "0"}
                  className="h-11 cursor-not-allowed rounded-xl border border-outline-variant bg-surface-container-low px-3 text-sm text-on-surface-variant outline-none"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-on-surface-variant">
                  Adjustment Type
                </label>
                <div className="flex items-center gap-4">
                  <label className="flex cursor-pointer items-center gap-2 text-sm text-on-surface-variant">
                    <input
                      type="radio"
                      name="adj_type"
                      checked={type === "decrease"}
                      onChange={() => setType("decrease")}
                      className="text-primary focus:ring-primary"
                    />
                    Decrease
                  </label>
                  <label className="flex cursor-pointer items-center gap-2 text-sm text-on-surface-variant">
                    <input
                      type="radio"
                      name="adj_type"
                      checked={type === "increase"}
                      onChange={() => setType("increase")}
                      className="text-primary focus:ring-primary"
                    />
                    Increase
                  </label>
                </div>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">
                  Adjustment Quantity
                </label>
                <input
                  type="number"
                  min="1"
                  placeholder="e.g. 50"
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, Number(e.target.value) || 1))}
                  className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed"
                />
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">
                  Reason
                </label>
                <select value={reason} onChange={(e) => setReason(e.target.value)} className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed">
                  <option>Damaged</option>
                  <option>Miscount</option>
                  <option>Return</option>
                  <option>Expired</option>
                  <option>Other</option>
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-on-surface-variant">
                  Notes
                </label>
                <textarea
                  rows="3"
                  placeholder="Add any relevant details..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="resize-none rounded-xl border border-outline-variant bg-surface-container-lowest px-3 py-2 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed"
                />
              </div>
            </div>

            {message && <p className="px-6 pb-2 text-sm text-error">{message}</p>}
            <div className="flex justify-end gap-3 border-t border-outline-variant bg-surface-container-lowest px-6 py-4">
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="h-11 rounded-xl border border-outline-variant px-5 text-sm font-medium text-on-surface-variant transition hover:bg-surface-container-low"
              >
                Cancel
              </button>
              <button
                type="button"
                className="h-11 rounded-xl bg-linear-to-r from-primary to-primary-container px-6 text-sm font-semibold text-on-primary shadow-md shadow-primary-fixed/50 transition hover:opacity-95"
              >
                Submit Adjustment
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default StockAdjustment;