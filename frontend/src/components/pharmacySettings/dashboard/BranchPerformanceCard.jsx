import { branchPerformance } from "../../../data/pharmacySettings/pharmacySettingsData";

const BranchPerformanceCard = () => (
  <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
    <h4 className="mb-4 text-xl font-semibold text-on-background">Branch Performance</h4>
    <div className="space-y-4">
      {branchPerformance.map(({ name, score }) => (
        <div key={name} className="space-y-1">
          <div className="flex justify-between text-xs font-semibold text-on-surface-variant">
            <span>{name}</span>
            <span className="font-bold text-on-background">{score}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-surface-container-high">
            <div
              className="h-full rounded-full bg-primary"
              style={{ width: `${score}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default BranchPerformanceCard;