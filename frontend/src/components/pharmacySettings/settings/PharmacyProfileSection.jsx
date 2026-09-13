import { useState } from "react";
import TabBar from "../common/TabBar";
import FormActions from "../common/FormActions";
import BusinessInfoTab from "./tabs/BusinessInfoTab";
import OwnerDetailsTab from "./tabs/OwnerDetailsTab";
import AddressTab from "./tabs/AddressTab";
import LicenseTab from "./tabs/LicenseTab";
import ContactInfoTab from "./tabs/ContactInfoTab";
import DocumentsTab from "./tabs/DocumentsTab";

const profileTabs = [
  { id: "business", label: "Business Information" },
  { id: "owner", label: "Owner Details" },
  { id: "address", label: "Pharmacy Address" },
  { id: "license", label: "License & Registration" },
  { id: "contact", label: "Contact Information" },
  { id: "documents", label: "Documents" },
];

const tabContentMap = {
  business: BusinessInfoTab,
  owner: OwnerDetailsTab,
  address: AddressTab,
  license: LicenseTab,
  contact: ContactInfoTab,
  documents: DocumentsTab,
};

const PharmacyProfileSection = () => {
  const [activeTab, setActiveTab] = useState("business");
  const ActiveTabContent = tabContentMap[activeTab];

  return (
    <section className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="p-8">
        <TabBar tabs={profileTabs} activeTab={activeTab} onChange={setActiveTab} />
        <ActiveTabContent />
        {activeTab !== "documents" && <FormActions />}
      </div>
    </section>
  );
};

export default PharmacyProfileSection;