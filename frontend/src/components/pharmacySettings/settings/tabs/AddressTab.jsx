import FormField from "../../common/FormField";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const timeZoneOptions = [
  "(GMT+05:30) India Standard Time",
  "(GMT+00:00) UTC",
  "(GMT-05:00) Eastern Time",
];

const AddressTab = () => {
  const { address } = pharmacyProfile;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Address Line 1" defaultValue={address.line1} />
      <FormField label="Address Line 2" defaultValue={address.line2} />
      <FormField label="Landmark" placeholder="Near Apollo Hospital" />
      <FormField label="City" defaultValue={address.city} />
      <FormField label="District" defaultValue={address.district} />
      <FormField label="State" defaultValue={address.state} />
      <FormField label="PIN Code" defaultValue={address.pinCode} />
      <FormField label="Country" defaultValue={address.country} />
      <FormField
        label="Time Zone"
        type="select"
        options={timeZoneOptions}
        defaultValue={address.timeZone}
      />
    </div>
  );
};

export default AddressTab;