import { useState } from "react";
import DirectorySearchPanel from "./DirectorySearchPanel";
import BranchCards from "./BranchCards";
import BranchDeepDive from "./BranchDeepDive";
import { directoryBranches } from "../../../data/pharmacySettings/pharmacySettingsData";

const BranchDirectory = () => {
  const [selectedBranchId, setSelectedBranchId] = useState(
    directoryBranches.find((branch) => branch.selected)?.id ?? directoryBranches[0].id
  );

  return (
    <>
      <DirectorySearchPanel />
      <BranchCards selectedId={selectedBranchId} onSelect={setSelectedBranchId} />
      <BranchDeepDive />
    </>
  );
};

export default BranchDirectory;