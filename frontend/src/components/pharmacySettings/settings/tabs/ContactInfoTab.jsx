import FormField from "../../common/FormField";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const ContactInfoTab = () => {
  const { contact } = pharmacyProfile;

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Business Phone Number" defaultValue={contact.businessPhone} />
      <FormField label="Alternate Phone Number" defaultValue={contact.alternatePhone} />
      <FormField label="Email Address" type="email" defaultValue={contact.email} />
      <FormField label="Website" defaultValue={contact.website} />
      <FormField
        label="Emergency Contact Number"
        defaultValue={contact.emergencyContact}
      />
      <FormField label="Customer Support Number" defaultValue={contact.supportNumber} />
      <FormField label="Opening Time" type="time" defaultValue={contact.openingTime} />
      <FormField label="Closing Time" type="time" defaultValue={contact.closingTime} />
    </div>
  );
};

export default ContactInfoTab;