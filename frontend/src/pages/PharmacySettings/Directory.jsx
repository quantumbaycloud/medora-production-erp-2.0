import { Link } from "react-router-dom";
import { ChevronRight, Plus, Printer } from "lucide-react";
import PageHeader from "../../components/pharmacySettings/common/PageHeader";
import DirectorySummary from "../../components/pharmacySettings/directory/DirectorySummary";
import BranchDirectory from "../../components/pharmacySettings/directory/BranchDirectory";

const Directory = () => {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Pharmacy & Branch Directory"
        description="Search and view complete pharmacy and branch information from a single dashboard."
        actions={
          <>
            <button
              type="button"
              className="flex items-center gap-2 rounded-xl border border-outline-variant px-4 py-2 text-sm font-semibold text-on-surface-variant transition-colors hover:bg-surface-container-low"
            >
              <Printer size={18} />
              Print Details
            </button>
            <button
              type="button"
              className="flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-on-primary shadow-sm transition-colors hover:bg-primary-container"
            >
              <Plus size={18} />
              Add New Branch
            </button>
          </>
        }
      />

      <nav className="flex items-center gap-2 text-xs font-semibold text-on-surface-variant" aria-label="Breadcrumb">
        <Link to="/pharmacy" className="transition-colors hover:text-primary">
          Dashboard
        </Link>
        <ChevronRight size={14} />
        <span className="text-on-background">Pharmacy Directory</span>
      </nav>

      <DirectorySummary />
      <BranchDirectory />
    </div>
  );
};

export default Directory;