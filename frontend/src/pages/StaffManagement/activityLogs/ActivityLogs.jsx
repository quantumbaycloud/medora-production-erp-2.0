import activityLogs from "../../../data/staffManagement/activityLogsData";

import ActivityLogsHeader from "../../../components/staffManagement/activityLogs/ActivityLogsHeader";
import ActivityLogsFilters from "../../../components/staffManagement/activityLogs/ActivityLogsFilters";
import ActivityLogsTable from "../../../components/staffManagement/activityLogs/ActivityLogsTable";
import ActivityLogsStatsCards from "../../../components/staffManagement/activityLogs/ActivityLogsStatsCards";

const ActivityLogs = () => {
  return (
    <div className="space-y-6 pb-12">
      <ActivityLogsHeader />

      <ActivityLogsFilters />

      <ActivityLogsTable logs={activityLogs} />

      <ActivityLogsStatsCards />
    </div>
  );
};

export default ActivityLogs;