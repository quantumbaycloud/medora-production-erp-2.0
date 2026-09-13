import { categoryDistribution } from "../../../data/pharmacySettings/pharmacySettingsData";

const CategoryDistributionCard = () => (
  <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
    <h4 className="mb-4 text-xl font-semibold text-on-background">Category Distribution</h4>
    <div className="relative flex h-40 items-center justify-center">
      <div className="h-32 w-32 rounded-full border-[16px] border-surface-container-high border-t-primary border-r-outline" />
      <div className="absolute flex flex-col items-center">
        <span className="text-2xl font-bold text-on-background">
          {categoryDistribution.totalSkus}
        </span>
        <span className="text-[10px] font-bold uppercase tracking-wide text-on-surface-variant">
          SKUs
        </span>
      </div>
    </div>
    <div className="mt-4 grid grid-cols-2 gap-2">
      {categoryDistribution.categories.map(({ name, color }) => (
        <span
          key={name}
          className="flex items-center gap-2 text-xs font-semibold text-on-surface-variant"
        >
          <span className={`h-2 w-2 rounded-full ${color}`} />
          {name}
        </span>
      ))}
    </div>
  </div>
);

export default CategoryDistributionCard;