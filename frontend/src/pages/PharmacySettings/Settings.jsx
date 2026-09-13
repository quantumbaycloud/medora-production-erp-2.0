import { useState } from "react";
import PageHeader from "../../components/pharmacySettings/common/PageHeader";
import SettingsNavCards from "../../components/pharmacySettings/settings/SettingsNavCards";
import PharmacyProfileSection from "../../components/pharmacySettings/settings/PharmacyProfileSection";
import BranchManagementSection from "../../components/pharmacySettings/settings/BranchManagementSection";

const Settings = () => {
  const [activeSection, setActiveSection] = useState("branch");

  return (
    <div>
      <PageHeader
        title="Pharmacy Settings"
        description="Configure your pharmacy's core identity, branch hierarchy, and operational parameters for global inventory management."
      />

      <SettingsNavCards activeSection={activeSection} onSelect={setActiveSection} />

      {activeSection === "profile" ? (
        <PharmacyProfileSection />
      ) : (
        <BranchManagementSection />
      )}
    </div>
  );
};

export default Settings;