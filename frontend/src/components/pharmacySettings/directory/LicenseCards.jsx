import { BadgeCheck, Download, FileText, Stamp } from "lucide-react";
import { directorySummary } from "../../../data/pharmacySettings/pharmacySettingsData";

const licenseIconMap = {
  "badge-check": BadgeCheck,
  "file-text": FileText,
  stamp: Stamp,
};

const licenseToneMap = {
  primary: "bg-primary/10 text-primary",
  secondary: "bg-secondary-container text-on-secondary-fixed-variant",
  tertiary: "bg-primary-fixed text-on-primary-fixed-variant",
};

const LicenseCards = () => (
  <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
    {directorySummary.licenses.map((license) => {
      const Icon = licenseIconMap[license.icon] ?? BadgeCheck;

      return (
        <div
          key={license.name}
          className="flex items-center gap-4 rounded-2xl border border-outline-variant bg-surface-container-lowest p-5"
        >
          <span
            className={`flex h-12 w-12 items-center justify-center rounded-xl ${licenseToneMap[license.tone]}`}
          >
            <Icon size={22} />
          </span>
          <div>
            <h4 className="text-xs font-bold text-on-background">{license.name}</h4>
            <p className="text-sm font-bold text-primary">{license.number}</p>
            <p className="text-[10px] text-on-surface-variant">{license.note}</p>
          </div>
          <button
            type="button"
            aria-label={`Download ${license.name}`}
            className="ml-auto text-on-surface-variant transition-colors hover:text-primary"
          >
            <Download size={18} />
          </button>
        </div>
      );
    })}
  </section>
);

export default LicenseCards;