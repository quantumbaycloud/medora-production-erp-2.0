import { moduleNavigation } from "../../data/navigation/navigationData";
import ModuleLayout from "../shared/ModuleLayout";

const SupplierManagementLayout = () => {
  return <ModuleLayout navigation={moduleNavigation.supplier} />;
};

export default SupplierManagementLayout;
