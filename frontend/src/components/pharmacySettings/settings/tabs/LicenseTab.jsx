import { Upload } from "lucide-react";
import FormField from "../../common/FormField";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const licenseUploads = ["Drug License", "GST Certificate", "Reg. Certificate"];

const LicenseTab = () => {
  const { license } = pharmacyProfile;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Drug License Number" defaultValue={license.drugLicenseNumber} />
      <FormField label="Drug License Issue Date" type="date" defaultValue={license.issueDate} />
      <FormField label="Drug License Expiry Date" type="date" defaultValue={license.expiryDate} />
      <FormField label="GST Number" defaultValue={license.gstNumber} />
      <FormField
        label="GST Registration Date"
        type="date"
        defaultValue={license.gstRegistrationDate}
      />
      <FormField
        label="Pharmacy Registration Number"
        defaultValue={license.registrationNumber}
      />
      <FormField label="FSSAI Number (Optional)" placeholder="14-digit FSSAI number" />

      <div className="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-3 md:col-span-2">
        {licenseUploads.map((label) => (
          <div key={label} className="flex flex-col gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-on-surface-variant">
              {label}
            </span>
            <button
              type="button"
              className="flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-outline-variant p-4 transition-colors hover:bg-surface-container-low"
            >
              <Upload size={18} className="mb-1 text-secondary" />
              <span className="text-[10px] font-bold uppercase text-secondary">Upload</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LicenseTab;