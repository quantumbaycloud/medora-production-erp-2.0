import { Link } from "react-router-dom";
import {
  Building2,
  Mail,
  Phone,
  Eye,
  Edit,
  Star,
  ArrowUpRight
} from "lucide-react";

const CATEGORY_STYLES = {
  Pharmaceuticals: {
    avatarBg: "bg-gradient-to-br from-blue-500 to-cyan-400",
    chipBg: "bg-primary-fixed text-primary ring-1 ring-primary-fixed-dim",
    accentBar: "from-blue-500 to-cyan-400",
    iconColor: "text-primary"
  },
  "Medical Equipment": {
    avatarBg: "bg-gradient-to-br from-violet-500 to-purple-400",
    chipBg: "bg-violet-50 text-violet-700 ring-1 ring-violet-200",
    accentBar: "from-violet-500 to-purple-400",
    iconColor: "text-violet-600"
  },
  "Reagents & Kits": {
    avatarBg: "bg-gradient-to-br from-emerald-500 to-teal-400",
    chipBg: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
    accentBar: "from-emerald-500 to-teal-400",
    iconColor: "text-secondary"
  },
  Consumables: {
    avatarBg: "bg-gradient-to-br from-amber-500 to-orange-400",
    chipBg: "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim",
    accentBar: "from-amber-500 to-orange-400",
    iconColor: "text-tertiary"
  }
};

const STATUS_STYLES = {
  Active: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
  "Pending Review": "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim",
  Inactive: "bg-surface-container text-on-surface-variant ring-1 ring-outline-variant"
};

const STATUS_DOT = {
  Active: "bg-secondary-container0",
  "Pending Review": "bg-tertiary-fixed0",
  Inactive: "bg-slate-400"
};

const SupplierCard = ({ supplier, onEditClick }) => {
  const categoryStyle =
    CATEGORY_STYLES[supplier.category] || CATEGORY_STYLES.Pharmaceuticals;

  return (
    <div className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-blue-300 hover:shadow-xl hover:shadow-blue-100/50">
      <div
        className={`absolute inset-x-0 top-0 h-1 bg-gradient-to-r ${categoryStyle.accentBar}`}
      />

      <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-gradient-to-br from-primary-fixed/40 to-teal-100/40 blur-2xl transition-opacity duration-300 opacity-60 group-hover:opacity-100" />

      <div className="relative p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <div
              className={`flex h-12 w-12 items-center justify-center rounded-xl text-lg font-bold text-on-primary shadow-md ${categoryStyle.avatarBg}`}
            >
              {supplier.name.charAt(0)}
            </div>
            <div>
              <h3 className="font-bold text-on-background transition group-hover:text-primary">
                {supplier.name}
              </h3>
              <p className="font-mono text-xs text-outline">{supplier.code}</p>
            </div>
          </div>

          <span
            className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
              STATUS_STYLES[supplier.status] || STATUS_STYLES.Inactive
            }`}
          >
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                STATUS_DOT[supplier.status] || STATUS_DOT.Inactive
              }`}
            />
            {supplier.status}
          </span>
        </div>

        <div className="mt-4 flex items-center justify-between">
          <span
            className={`inline-flex items-center rounded-lg px-2.5 py-1 text-xs font-semibold ${categoryStyle.chipBg}`}
          >
            {supplier.category}
          </span>

          <span className="inline-flex items-center gap-1 text-xs font-semibold text-tertiary">
            <Star size={13} className="fill-amber-400 text-amber-400" />
            {supplier.rating}
          </span>
        </div>

        <div className="mt-4 space-y-2.5 text-xs text-on-surface-variant">
          <div className="flex items-center gap-2.5">
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-surface-container-low ring-1 ring-slate-100">
              <Building2 size={13} className={categoryStyle.iconColor} />
            </div>
            <span className="font-medium text-on-surface-variant">
              {supplier.contactPerson}
            </span>
          </div>
          <div className="flex items-center gap-2.5">
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-surface-container-low ring-1 ring-slate-100">
              <Mail size={13} className="text-on-surface-variant" />
            </div>
            <span className="truncate">{supplier.email}</span>
          </div>
          <div className="flex items-center gap-2.5">
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-surface-container-low ring-1 ring-slate-100">
              <Phone size={13} className="text-on-surface-variant" />
            </div>
            <span>{supplier.phone}</span>
          </div>
        </div>
      </div>

      <div className="relative mt-2 flex items-center justify-between gap-2 border-t border-slate-100 bg-surface-container-low/50 px-5 py-4">
        <div>
          <span className="block text-[11px] font-medium uppercase tracking-wider text-outline">
            Outstanding
          </span>
          <span className="font-mono text-sm font-bold text-on-background">
            {supplier.balance}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to={`/suppliers/${supplier.id}`}
            state={{ supplier }}
            className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-3.5 py-2 text-xs font-semibold text-on-primary shadow-sm transition hover:opacity-95 hover:shadow-md"
          >
            <Eye size={13} />
            <span>Profile</span>
            <ArrowUpRight size={12} className="opacity-70" />
          </Link>

          <button
            onClick={() => onEditClick(supplier)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-outline-variant bg-surface-container-lowest px-3.5 py-2 text-xs font-semibold text-on-surface-variant shadow-sm transition hover:border-blue-300 hover:bg-primary-fixed hover:text-primary"
          >
            <Edit size={13} />
            <span>Manage</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SupplierCard;
