import { Link } from "react-router-dom";
import { ArrowLeft, Pencil, Star } from "lucide-react";

const STATUS_STYLES = {
  Active: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
  "Pending Review": "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim",
  Inactive: "bg-surface-container text-on-surface-variant ring-1 ring-outline-variant"
};

const SupplierProfileHeader = ({ supplier, onEditClick }) => {
  return (
    <div className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-start gap-4">
          <Link
            to="/suppliers"
            className="mt-1 inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-outline-variant bg-surface-container-low text-on-surface-variant transition hover:bg-surface-container hover:text-on-surface-variant"
            aria-label="Back to suppliers"
          >
            <ArrowLeft size={18} />
          </Link>

          <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-50 to-teal-50 text-2xl font-bold text-primary ring-1 ring-primary-fixed">
            {supplier.name.charAt(0)}
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="text-2xl font-bold tracking-tight text-on-background">
                {supplier.name}
              </h1>
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${STATUS_STYLES[supplier.status] || STATUS_STYLES.Inactive}`}
              >
                {supplier.status}
              </span>
            </div>

            <div className="mt-1.5 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-on-surface-variant">
              <span className="font-mono text-xs text-outline">
                {supplier.code}
              </span>
              <span className="inline-flex items-center gap-1 rounded-md bg-surface-container px-2 py-0.5 text-xs font-semibold text-on-surface-variant">
                {supplier.category}
              </span>
              <span className="inline-flex items-center gap-1 text-tertiary">
                <Star size={14} className="fill-amber-400 text-amber-400" />
                <span className="font-semibold text-on-surface-variant">
                  {supplier.rating}
                </span>
                <span className="text-xs text-outline">/ 5.0</span>
              </span>
            </div>

            <p className="mt-3 max-w-2xl text-sm leading-relaxed text-on-surface-variant">
              {supplier.description}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2 lg:flex-col lg:items-stretch">
          <button
            onClick={onEditClick}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-on-primary shadow-md transition hover:opacity-95 focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <Pencil size={16} />
            <span>Edit Profile</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SupplierProfileHeader;