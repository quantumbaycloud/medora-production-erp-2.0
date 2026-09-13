import { Search, Store } from "lucide-react";

const quickFilters = ["Active", "Inactive", "Verified", "Unverified"];

const DirectorySearchPanel = () => (
  <section className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
    <div className="grid grid-cols-1 items-end gap-4 md:grid-cols-4">
      <div className="space-y-2">
        <label htmlFor="search-pharmacy" className="block text-xs font-bold text-on-background">
          Search Pharmacy
        </label>
        <div className="relative">
          <Store size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-primary" />
          <input
            id="search-pharmacy"
            type="text"
            defaultValue="Medorax Central"
            className="h-11 w-full rounded-xl border border-outline-variant bg-surface-container-lowest pl-10 pr-4 text-sm text-on-surface focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10"
          />
        </div>
      </div>

      <div className="space-y-2">
        <label htmlFor="search-branch" className="block text-xs font-bold text-on-background">
          Search Branch
        </label>
        <div className="relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-outline" />
          <input
            id="search-branch"
            type="text"
            placeholder="Branch Name or ID..."
            className="h-11 w-full rounded-xl border border-outline-variant bg-surface-container-lowest pl-10 pr-4 text-sm text-on-surface placeholder:text-outline focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10"
          />
        </div>
      </div>

      <div className="flex gap-2 md:col-span-2">
        <button
          type="button"
          className="flex h-11 flex-1 items-center justify-center gap-2 rounded-xl bg-primary font-bold text-on-primary shadow-md transition-colors hover:bg-primary-container"
        >
          <Search size={18} />
          Search
        </button>
        <button
          type="button"
          className="h-11 rounded-xl border border-outline-variant px-6 font-bold text-on-surface-variant transition-colors hover:bg-surface-container-low"
        >
          Reset Filters
        </button>
      </div>
    </div>

    <div className="mt-4 flex flex-wrap items-center gap-2">
      <span className="mr-2 text-xs font-semibold text-on-surface-variant">Quick Filters:</span>
      {quickFilters.map((filter, index) => (
        <button
          key={filter}
          type="button"
          aria-pressed={index === 0}
          className={`rounded-full border px-4 py-1.5 text-xs font-bold transition-colors ${
            index === 0
              ? "border-primary/20 bg-primary/10 text-primary"
              : "border-outline-variant bg-surface-container-low text-on-surface-variant hover:border-primary/50"
          }`}
        >
          {filter}
        </button>
      ))}
    </div>
  </section>
);

export default DirectorySearchPanel;