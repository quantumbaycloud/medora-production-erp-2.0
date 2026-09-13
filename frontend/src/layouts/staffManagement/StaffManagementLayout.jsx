import { moduleNavigation } from "../../data/navigation/navigationData";
import ModuleLayout from "../shared/ModuleLayout";

const StaffManagementLayout = () => {
  return <ModuleLayout navigation={moduleNavigation.staff} />;
};

export default StaffManagementLayout;
