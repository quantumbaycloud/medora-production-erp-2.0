import FormField from "../../common/FormField";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const businessTypeOptions = ["Retail Pharmacy", "Wholesale", "Hospital Internal"];

const BusinessInfoTab = () => {
  const { business } = pharmacyProfile;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Pharmacy Name" defaultValue={business.pharmacyName} />
      <FormField
        label="Business Type"
        type="select"
        options={businessTypeOptions}
        defaultValue={business.businessType}
      />
      <FormField label="GST Number" defaultValue={business.gstNumber} />
      <FormField label="Drug License Number" defaultValue={business.drugLicenseNumber} />
      <FormField label="PAN Number" defaultValue={business.panNumber} />
      <FormField
        label="Pharmacy Registration Number"
        defaultValue={business.registrationNumber}
      />
      <FormField label="Establishment Date" type="date" defaultValue={business.establishmentDate} />

      <div className="flex flex-col gap-1.5">
        <span className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
          Pharmacy Logo
        </span>
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-lg border border-outline-variant bg-surface-container-low text-xs font-bold text-on-surface-variant">
            MC
          </span>
          <button
            type="button"
            className="rounded-xl border border-outline-variant px-4 py-2 text-xs font-bold uppercase text-primary transition-colors hover:bg-surface-container-low"
          >
            Upload Logo
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-1.5 md:col-span-2">
        <label
          htmlFor="pharmacy-description"
          className="text-xs font-bold uppercase tracking-wider text-on-surface-variant"
        >
          Pharmacy Description
        </label>
        <textarea
          id="pharmacy-description"
          rows={4}
          defaultValue={business.description}
          className="w-full rounded-xl border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-sm text-on-surface focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10"
        />
      </div>
    </div>
  );
};

export default BusinessInfoTab;