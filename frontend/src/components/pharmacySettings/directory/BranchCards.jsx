import StatusChip from "../common/StatusChip";
import { directoryBranches } from "../../../data/pharmacySettings/pharmacySettingsData";

const branchStatusTone = {
  ACTIVE: "success",
  INACTIVE: "error",
};

const BranchCards = ({ selectedId, onSelect }) => (
  <section className="space-y-4">
    <div className="flex items-center justify-between">
      <h3 className="text-lg font-bold text-on-background">
        Branch Directory ({String(directoryBranches.length).padStart(2, "0")})
      </h3>
    </div>

    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {directoryBranches.map((branch) => {
        const isSelected = branch.id === selectedId;
        const isActive = branch.status === "ACTIVE";

        return (
          <button
            key={branch.id}
            type="button"
            onClick={() => onSelect(branch.id)}
            aria-pressed={isSelected}
            className={`overflow-hidden rounded-2xl border bg-surface-container-lowest text-left transition-shadow hover:shadow-md ${
              isSelected ? "border-primary ring-1 ring-primary/20" : "border-outline-variant"
            } ${isActive ? "" : "opacity-70 grayscale"}`}
          >
            <div
              className={`flex items-center justify-between border-b border-outline-variant p-5 ${
                isSelected ? "bg-primary/5" : "bg-surface-container-low"
              }`}
            >
              <div>
                <h4 className="font-bold text-on-background">{branch.name}</h4>
                <p className="text-xs font-semibold text-on-surface-variant">Code: {branch.id}</p>
              </div>
              <StatusChip tone={branchStatusTone[branch.status]}>{branch.status}</StatusChip>
            </div>

            <div className="space-y-3 p-5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-on-surface-variant">Manager</span>
                <span className="font-bold text-on-background">{branch.manager}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-on-surface-variant">Contact</span>
                <span className="font-bold text-on-background">{branch.contact}</span>
              </div>
              <div className="pt-2">
                <span
                  className={`block w-full rounded-xl py-2 text-center text-xs font-bold transition-colors ${
                    isSelected
                      ? "bg-primary text-on-primary"
                      : "border border-outline-variant text-on-surface hover:bg-surface-container-low"
                  }`}
                >
                  {isSelected
                    ? "Currently Selected"
                    : isActive
                      ? "View Details"
                      : "Re-activate"}
                </span>
              </div>
            </div>
          </button>
        );
      })}
    </div>
  </section>
);

export default BranchCards;