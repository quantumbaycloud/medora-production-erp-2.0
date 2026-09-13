import attendanceRecords from "../../../data/staffManagement/attendanceData";

import AttendanceHeader from "../../../components/staffManagement/attendance/AttendanceHeader";
import AttendanceFilters from "../../../components/staffManagement/attendance/AttendanceFilters";
import AttendanceTable from "../../../components/staffManagement/attendance/AttendanceTable";
import AttendanceStatsCards from "../../../components/staffManagement/attendance/AttendanceStatsCards";

const Attendance = () => {
  return (
    <div className="space-y-6 pb-12">
      <AttendanceHeader />

      <AttendanceFilters />

      <AttendanceTable records={attendanceRecords} />

      <AttendanceStatsCards />
    </div>
  );
};

export default Attendance;