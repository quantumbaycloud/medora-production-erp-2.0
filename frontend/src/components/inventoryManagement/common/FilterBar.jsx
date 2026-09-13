import { Search, RefreshCw, Download, Plus } from "lucide-react";

const FilterBar = ({
  searchPlaceholder = "Search by Name, SKU, or Code...",
  categories = [],
  warehouses = [],
  actionLabel = "Add",
  actionIcon: ActionIcon = Plus,
  onAction,
  showExport = true,
}) => {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-outline-variant bg-surface-container-lowest p-4 shadow-sm md:flex-row md:items-center md:justify-between">
      <div className="relative w-full md:w-auto md:flex-1">
        <Search
          size={18}
          className="absolute left-3.5 top-1/2 -translate-y-1/2 text-outline"
        />
        <input
          type="text"
          placeholder={searchPlaceholder}
          className="h-11 w-full rounded-xl border border-outline-variant bg-surface-container-low pl-11 pr-4 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary-fixed"
        />
      </div>

      <div className="flex w-full flex-col gap-3 sm:flex-row md:w-auto">
        {categories.length > 0 && (
          <select className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed md:w-44">
            <option value="">All Categories</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        )}

        {warehouses.length > 0 && (
          <select className="h-11 rounded-xl border border-outline-variant bg-surface-container-lowest px-3 text-sm text-on-surface-variant outline-none transition focus:border-primary focus:ring-2 focus:ring-primary-fixed md:w-44">
            <option value="">All Warehouses</option>
            {warehouses.map((warehouse) => (
              <option key={warehouse} value={warehouse}>
                {warehouse}
              </option>
            ))}
          </select>
        )}

        <button
          type="button"
          className="flex h-11 w-11 items-center justify-center rounded-xl border border-outline-variant text-on-surface-variant transition hover:bg-surface-container-low hover:text-primary"
          aria-label="Refresh"
        >
          <RefreshCw size={18} />
        </button>

        {showExport && (
          <button
            type="button"
            className="flex h-11 items-center justify-center gap-2 rounded-xl border border-primary-fixed-dim bg-surface-container-lowest px-4 text-sm font-medium text-primary transition hover:bg-primary-fixed"
          >
            <Download size={17} />
            Export CSV
          </button>
        )}

        <button
          type="button"
          onClick={onAction}
          className="flex h-11 items-center justify-center gap-2 rounded-xl bg-primary px-5 text-sm font-semibold text-on-primary shadow-md shadow-primary/20 transition hover:opacity-95"
        >
          <ActionIcon size={17} />
          {actionLabel}
        </button>
      </div>
    </div>
  );
};

export default FilterBar;
