import { useState } from "react";
import FormField from "../../common/FormField";
import FormActions from "../../common/FormActions";
import { branches } from "../../../../data/pharmacySettings/pharmacySettingsData";

const businessTypeOptions = ["Retail Pharmacy", "Wholesale", "Clinic Pharmacy"];

const EditBranchTab = () => {
  const [selectedBranchId, setSelectedBranchId] = useState(branches[1].id);
  const selectedBranch = branches.find((branch) => branch.id === selectedBranchId);

  return (
    <div>
      <div className="mb-8 rounded-xl border border-outline-variant bg-surface-container-low p-4">
        <label
          htmlFor="edit-branch-select"
          className="mb-2 block text-xs font-bold uppercase tracking-wider text-on-surface-variant"
        >
          Select Branch to Edit
        </label>
        <select
          id="edit-branch-select"
          value={selectedBranchId}
          onChange={(event) => setSelectedBranchId(event.target.value)}
          className="h-11 w-full rounded-xl border border-outline-variant bg-surface-container-lowest px-4 text-sm text-on-surface focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10"
        >
          {branches.map((branch) => (
            <option key={branch.id} value={branch.id}>
              {branch.name} ({branch.code})
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <FormField label="Branch Name" defaultValue={selectedBranch.name} />
        <FormField label="Branch Code" defaultValue={selectedBranch.code} />
        <FormField label="Manager Name" defaultValue={selectedBranch.manager} />
        <FormField label="Contact Number" defaultValue={selectedBranch.contact} />
        <FormField label="Email Address" type="email" defaultValue={selectedBranch.email} />
        <FormField
          label="Business Type"
          type="select"
          options={businessTypeOptions}
          defaultValue={selectedBranch.businessType}
        />
        <div className="md:col-span-2">
          <FormField label="Address Line 1" defaultValue={selectedBranch.addressLine1} />
        </div>
        <FormField label="City" defaultValue={selectedBranch.city} />
        <FormField label="State" defaultValue={selectedBranch.state} />
        <FormField label="PIN Code" defaultValue={selectedBranch.pinCode} />
      </div>
      <FormActions />
    </div>
  );
};

export default EditBranchTab;