import { Eye, Mail, Phone } from "lucide-react";
import { directorySummary } from "../../../data/pharmacySettings/pharmacySettingsData";

const OwnerInfoCard = () => {
  const { owner } = directorySummary;

  return (
    <div className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
      <div className="mb-6 flex items-center gap-4">
        <img
          src="https://i.pravatar.cc/100?img=12"
          alt={owner.name}
          className="h-16 w-16 rounded-full object-cover ring-2 ring-primary/20"
        />
        <div>
          <h3 className="font-bold text-on-background">{owner.name}</h3>
          <p className="text-sm text-on-surface-variant">{owner.role}</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="space-y-2 rounded-xl border border-outline-variant bg-surface p-3">
          <p className="flex items-center gap-3 text-sm text-on-surface">
            <Phone size={18} className="text-primary" /> {owner.phone}
          </p>
          <p className="flex items-center gap-3 text-sm text-on-surface">
            <Mail size={18} className="text-primary" /> {owner.email}
          </p>
        </div>

        <div className="space-y-3 px-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-on-surface-variant">Aadhaar (Masked)</span>
            <span className="flex items-center gap-2">
              <span className="text-xs font-bold text-on-background">{owner.aadhaarMasked}</span>
              <Eye size={14} className="text-primary" />
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-on-surface-variant">PAN Card</span>
            <span className="flex items-center gap-2">
              <span className="text-xs font-bold text-on-background">{owner.panMasked}</span>
              <Eye size={14} className="text-primary" />
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OwnerInfoCard;