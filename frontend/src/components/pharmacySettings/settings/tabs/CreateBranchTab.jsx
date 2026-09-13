import FormField from "../../common/FormField";
import FormActions from "../../common/FormActions";

const businessTypeOptions = ["Retail Pharmacy", "Wholesale", "Clinic Pharmacy"];

const CreateBranchTab = () => (
  <div>
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
      <FormField label="Branch Name" placeholder="Enter branch name" />
      <FormField label="Branch Code" placeholder="e.g. BR-003" />
      <FormField label="Manager Name" placeholder="Full name" />
      <FormField label="Contact Number" placeholder="+91" />
      <FormField label="Email Address" type="email" placeholder="branch@medorax.com" />
      <FormField label="Business Type" type="select" options={businessTypeOptions} />
      <div className="md:col-span-2">
        <FormField label="Address Line 1" placeholder="Street address" />
      </div>
      <FormField label="City" />
      <FormField label="State" />
      <FormField label="PIN Code" />
    </div>
    <FormActions primaryLabel="Create Branch" />
  </div>
);

export default CreateBranchTab;