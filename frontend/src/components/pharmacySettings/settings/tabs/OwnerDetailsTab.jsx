import FormField from "../../common/FormField";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const genderOptions = ["Male", "Female", "Other"];

const OwnerDetailsTab = () => {
  const { owner } = pharmacyProfile;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Owner Full Name" defaultValue={owner.fullName} />
      <FormField label="Father's Name" defaultValue={owner.fatherName} />
      <FormField label="Date of Birth" type="date" defaultValue={owner.dateOfBirth} />
      <FormField
        label="Gender"
        type="select"
        options={genderOptions}
        defaultValue={owner.gender}
      />
      <FormField label="Aadhaar Number" defaultValue={owner.aadhaarNumber} />
      <FormField label="PAN Number" defaultValue={owner.panNumber} />
      <FormField label="Mobile Number" defaultValue={owner.mobileNumber} />
      <FormField
        label="Alternate Mobile Number"
        defaultValue={owner.alternateMobileNumber}
      />
      <FormField label="Email Address" type="email" defaultValue={owner.email} />

      <div className="flex flex-col gap-1.5">
        <span className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
          Owner Photo
        </span>
        <div className="flex items-center gap-3">
          <img
            src="https://i.pravatar.cc/100?img=12"
            alt="Owner portrait"
            className="h-10 w-10 rounded-full border border-outline-variant object-cover"
          />
          <button
            type="button"
            className="rounded-xl border border-outline-variant px-4 py-2 text-xs font-bold uppercase text-primary transition-colors hover:bg-surface-container-low"
          >
            Upload Photo
          </button>
        </div>
      </div>
    </div>
  );
};

export default OwnerDetailsTab;