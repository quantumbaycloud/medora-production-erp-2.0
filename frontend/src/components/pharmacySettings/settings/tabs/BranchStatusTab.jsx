import StatusChip from "../../common/StatusChip";
import { branches } from "../../../../data/pharmacySettings/pharmacySettingsData";

const statusTone = {
  Active: "success",
  "Temporarily Closed": "warning",
};

const BranchStatusTab = () => (
  <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
    {branches.map((branch) => (
      <div
        key={branch.id}
        className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 transition-shadow hover:shadow-md"
      >
        <div className="mb-4 flex items-start justify-between">
          <div>
            <h6 className="text-lg font-bold text-on-background">{branch.name}</h6>
            <span className="text-xs text-on-surface-variant">{branch.code}</span>
          </div>
          <StatusChip tone={statusTone[branch.status]}>{branch.status}</StatusChip>
        </div>

        <div className="mb-6 space-y-2 text-sm text-on-surface-variant">
          <p>Manager: {branch.manager}</p>
          <p>{branch.contact}</p>
        </div>

        <div className="flex gap-2">
          <button
            type="button"
            className="flex-1 rounded-xl border border-outline-variant py-2 text-xs font-bold text-primary transition-colors hover:bg-surface-container-low"
          >
            View Details
          </button>
          {branch.status === "Active" ? (
            <button
              type="button"
              className="flex-1 rounded-xl bg-error-container py-2 text-xs font-bold text-on-error-container transition-colors hover:brightness-95"
            >
              Deactivate
            </button>
          ) : (
            <button
              type="button"
              className="flex-1 rounded-xl bg-secondary-container py-2 text-xs font-bold text-on-secondary-fixed-variant transition-colors hover:brightness-95"
            >
              Activate
            </button>
          )}
        </div>
      </div>
    ))}
  </div>
);

export default BranchStatusTab;