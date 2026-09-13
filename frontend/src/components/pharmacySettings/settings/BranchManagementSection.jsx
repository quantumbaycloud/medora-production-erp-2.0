import { useState } from "react";
import TabBar from "../common/TabBar";
import CreateBranchTab from "./tabs/CreateBranchTab";
import EditBranchTab from "./tabs/EditBranchTab";
import BranchSettingsTab from "./tabs/BranchSettingsTab";
import BranchStatusTab from "./tabs/BranchStatusTab";

const branchTabs = [
  { id: "create", label: "Create Branch" },
  { id: "edit", label: "Edit Branch" },
  { id: "settings", label: "Branch Settings" },
  { id: "status", label: "Branch Status" },
];

const tabContentMap = {
  create: CreateBranchTab,
  edit: EditBranchTab,
  settings: BranchSettingsTab,
  status: BranchStatusTab,
};

const BranchManagementSection = () => {
  const [activeTab, setActiveTab] = useState("create");
  const ActiveTabContent = tabContentMap[activeTab];

  return (
    <section className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="p-8">
        <TabBar tabs={branchTabs} activeTab={activeTab} onChange={setActiveTab} />
        <ActiveTabContent />
      </div>
    </section>
  );
};

export default BranchManagementSection;