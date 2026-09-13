import { Outlet } from "react-router-dom";

import ModuleNavigation from "../../components/navigation/ModuleNavigation";

const ModuleLayout = ({ navigation }) => {
  return (
    <div className="mx-auto max-w-[1440px] space-y-6">
      <ModuleNavigation {...navigation} />
      <Outlet />
    </div>
  );
};

export default ModuleLayout;
