import { ChevronLeft, ChevronRight } from "lucide-react";

const Pagination = ({ currentPage = 1, totalPages = 98, totalEntries = 14285, pageSize = 5 }) => {
  const startEntry = (currentPage - 1) * pageSize + 1;
  const endEntry = Math.min(currentPage * pageSize, totalEntries);

  const getPageNumbers = () => {
    const pages = [];
    for (let i = 1; i <= Math.min(3, totalPages); i++) {
      pages.push(i);
    }
    if (totalPages > 3) {
      pages.push("...");
      pages.push(totalPages);
    }
    return pages;
  };

  return (
    <div className="flex flex-col gap-4 border-t border-outline-variant bg-surface-container-lowest p-4 sm:flex-row sm:items-center sm:justify-between">
      <p className="text-sm text-on-surface-variant">
        Showing <span className="font-semibold text-on-background">{startEntry}</span> to{" "}
        <span className="font-semibold text-on-background">{endEntry}</span> of{" "}
        <span className="font-semibold text-on-background">{totalEntries.toLocaleString()}</span> entries
      </p>

      <div className="flex items-center gap-1.5">
        <button
          type="button"
          disabled={currentPage === 1}
          className="flex h-8 w-8 items-center justify-center rounded-lg border border-outline-variant text-on-surface-variant transition hover:bg-surface-container-low disabled:opacity-40"
          aria-label="Previous page"
        >
          <ChevronLeft size={18} />
        </button>

        {getPageNumbers().map((page, index) =>
          page === "..." ? (
            <span key={`ellipsis-${index}`} className="px-1 text-outline">
              ...
            </span>
          ) : (
            <button
              key={page}
              type="button"
              className={`flex h-8 w-8 items-center justify-center rounded-lg text-sm font-semibold transition ${
                page === currentPage
                  ? "bg-primary text-on-primary shadow-sm"
                  : "border border-outline-variant text-on-surface-variant hover:bg-surface-container-low"
              }`}
            >
              {page}
            </button>
          )
        )}

        <button
          type="button"
          disabled={currentPage === totalPages}
          className="flex h-8 w-8 items-center justify-center rounded-lg border border-outline-variant text-on-surface-variant transition hover:bg-surface-container-low disabled:opacity-40"
          aria-label="Next page"
        >
          <ChevronRight size={18} />
        </button>
      </div>
    </div>
  );
};

export default Pagination;
