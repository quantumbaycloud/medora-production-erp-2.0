import { moduleNavigation } from "../../data/navigation/navigationData";
import ModuleLayout from "../shared/ModuleLayout";

const InventoryLayout = () => {
  return <ModuleLayout navigation={moduleNavigation.inventory} />;
};

export default InventoryLayout;
