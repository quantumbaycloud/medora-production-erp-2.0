import { Search, Download, Users } from "lucide-react";
import { supplierData } from "../../../data/reports/mockData";
import SupplierRow from "./SupplierRow";

const SupplierTable = () => {
  const suppliers = supplierData.map((s) => ({ id: s.id, name: s.name, contact: s.contact_person || "—", balance: `₹${Number(s.outstanding_balance || 0).toLocaleString("en-IN")}`, status: Number(s.outstanding_balance || 0) > 0 ? "Outstanding" : "Current", statusClass: Number(s.outstanding_balance || 0) > 0 ? "bg-error-container text-on-error-container" : "bg-secondary-container text-on-secondary-fixed-variant" }));

  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-5 border-b border-outline-variant px-6 py-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-blue-50 to-teal-50 ring-1 ring-primary-fixed">
            <Users size={18} className="text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-on-background">
              Supplier Directory
            </h2>
            <p className="mt-0.5 text-sm text-on-surface-variant">
              View and manage all registered suppliers.
            </p>
          </div>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="relative">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-outline"
            />

            <input
              placeholder="Search suppliers..."
              className="h-11 w-full rounded-xl border border-outline-variant bg-surface-container-low pl-11 pr-4 text-sm outline-none transition focus:border-primary focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary-fixed sm:w-72"
            />
          </div>

          <button className="flex h-11 items-center justify-center gap-2 rounded-xl bg-primary px-5 text-sm font-medium text-on-primary shadow-md shadow-primary-fixed/50 transition hover:opacity-95 hover:shadow-lg">
            <Download size={17} />
            Export
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-surface-container-low">
            <tr className="text-sm text-on-surface-variant">
              <th className="px-6 py-4 text-left font-semibold">Supplier</th>
              <th className="px-6 py-4 text-left font-semibold">Contact</th>
              <th className="px-6 py-4 text-right font-semibold">Outstanding</th>
              <th className="px-6 py-4 text-center font-semibold">Status</th>
              <th className="px-6 py-4 text-right font-semibold">Action</th>
            </tr>
          </thead>

          <tbody>
            {suppliers.map((supplier, index) => (
              <SupplierRow
                key={supplier.id}
                supplier={supplier}
                index={index}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SupplierTable;
