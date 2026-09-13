import { Building2 } from "lucide-react";
import StatusChip from "../common/StatusChip";
import { directorySummary } from "../../../data/pharmacySettings/pharmacySettingsData";

const PharmacyInfoCard = () => {
  const { pharmacy } = directorySummary;

  const details = [
    { label: "GST Number", value: pharmacy.gstNumber },
    { label: "License No.", value: pharmacy.licenseNo },
    { label: "PAN Number", value: pharmacy.panNumber },
    { label: "Est. Date", value: pharmacy.establishedOn },
  ];

  return (
    <div className="flex flex-col justify-between rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
      <div>
        <div className="mb-6 flex items-start justify-between">
          <span className="flex h-16 w-16 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <Building2 size={32} />
          </span>
          <div className="flex flex-col items-end gap-1">
            {pharmacy.verified && <StatusChip tone="success">Verified</StatusChip>}
            <StatusChip tone={pharmacy.active ? "success" : "neutral"}>
              {pharmacy.active ? "Active" : "Inactive"}
            </StatusChip>
          </div>
        </div>

        <h3 className="text-xl font-bold text-on-background">{pharmacy.name}</h3>
        <p className="mb-4 mt-1 text-sm font-medium text-on-surface-variant">
          Code: {pharmacy.code}
        </p>

        <dl className="space-y-3 border-t border-outline-variant pt-4">
          {details.map(({ label, value }) => (
            <div key={label} className="flex justify-between">
              <dt className="text-xs font-semibold text-on-surface-variant">{label}</dt>
              <dd className="text-xs font-bold text-on-background">{value}</dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  );
};

export default PharmacyInfoCard;