import { Users, UserCheck, UserX, Building2, ArrowRight, Shield, Settings } from "lucide-react";
import { staffMembers } from "../../../data/staffManagement/staffData";
import attendanceRecords from "../../../data/staffManagement/attendanceData";
import activityLogs from "../../../data/staffManagement/activityLogsData";

export default function Dashboard() {
  const total = staffMembers.length;
  const present = attendanceRecords.filter((x) => x.check_out_at || x.status === "Present").length;
  const absent = Math.max(total - present, 0);
  const departments = new Set(staffMembers.map((x) => x.department || x.role?.name).filter(Boolean)).size;
  const pct = total ? Math.round((present / total) * 100) : 0;

  return <div className="space-y-8">
    <div><h2 className="text-3xl font-bold tracking-tight text-on-background">Staff Dashboard</h2><p className="mt-1 text-base text-on-surface-variant">Live staff and attendance data for the active pharmacy.</p></div>
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      {[[Users,"Total Employees",total,"bg-primary"],[UserCheck,"Present Today",present,`bg-secondary`],[UserX,"Absent / Open",absent,"bg-error"],[Building2,"Departments",departments,"bg-secondary"]].map(([Icon,label,value,bg])=><div key={label} className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6"><Icon size={40} className="mb-4 text-primary"/><span className="text-sm font-semibold uppercase tracking-wider text-on-surface-variant">{label}</span><div className="mt-2 text-4xl font-extrabold text-on-background">{value}</div><div className="mt-4 h-1 overflow-hidden rounded-full bg-surface-container"><div className={`h-full ${bg}`} style={{width:`${label==='Present Today'?pct:100}%`}}/></div></div>)}
    </div>
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
      <div className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest lg:col-span-2"><div className="flex items-center justify-between border-b border-outline-variant p-6"><h3 className="text-xl font-bold text-on-background">Recent Activity</h3><ArrowRight size={18} className="text-primary"/></div><div className="divide-y divide-outline-variant">{activityLogs.slice(0,10).map((item,i)=><div key={item.id||i} className="flex items-center gap-4 p-5"><div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-fixed text-primary"><Settings size={18}/></div><div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold text-on-background">{item.action_type || "System activity"}</p><p className="truncate text-xs text-on-surface-variant">{item.user_email || "System"} • {item.entity_type || "—"} • {item.created_at ? new Date(item.created_at).toLocaleString() : "—"}</p></div><Shield size={16} className="text-primary"/></div>)}</div>{activityLogs.length===0&&<div className="p-8 text-center text-sm text-on-surface-variant">No audit activity recorded yet.</div>}</div>
      <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6"><h4 className="mb-4 text-xl font-bold text-on-background">Attendance Coverage</h4><p className="mb-6 text-sm text-on-surface-variant">{pct}% of current staff have an attendance record for the loaded period.</p><div className="text-4xl font-extrabold text-primary">{pct}%</div><p className="mt-2 text-sm text-on-surface-variant">Present: {present} • Remaining: {absent}</p></div>
    </div>
  </div>;
}
