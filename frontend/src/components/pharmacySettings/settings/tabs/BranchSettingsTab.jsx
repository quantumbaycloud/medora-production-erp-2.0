import { useState } from "react";
import FormField from "../../common/FormField";
import FormActions from "../../common/FormActions";
import ToggleSwitch from "../../common/ToggleSwitch";
import { branches } from "../../../../data/pharmacySettings/pharmacySettingsData";

const taxSchemeOptions = ["Standard GST (18%)", "Reduced GST (12%)", "Exempt"];

const BranchSettingsTab = () => {
  const [selectedBranchId, setSelectedBranchId] = useState(branches[1].id);
  const selectedBranch = branches.find((branch) => branch.id === selectedBranchId);

  return (
    <div>
      <div className="mb-8 rounded-xl border border-outline-variant bg-surface-container-low p-4">
        <label
          htmlFor="settings-branch-select"
          className="mb-2 block text-xs font-bold uppercase tracking-wider text-on-surface-variant"
        >
          Select Branch for Settings
        </label>
        <select
          id="settings-branch-select"
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

      <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <ToggleSwitch
            label="Enable Billing"
            description="Allow this branch to generate invoices"
            defaultEnabled={selectedBranch.settings.billingEnabled}
          />
          <ToggleSwitch
            label="Auto-Stock Refill"
            description="Automatically trigger orders when stock is low"
            defaultEnabled={selectedBranch.settings.autoRefill}
          />
        </div>
        <div className="space-y-6">
          <FormField
            label="Inventory Threshold (%)"
            type="number"
            defaultValue={selectedBranch.settings.threshold}
          />
          <FormField
            label="Tax Configuration"
            type="select"
            options={taxSchemeOptions}
            defaultValue={selectedBranch.settings.taxScheme}
          />
        </div>
      </div>
      <FormActions primaryLabel="Save Settings" />
    </div>
  );
};

export default BranchSettingsTab;