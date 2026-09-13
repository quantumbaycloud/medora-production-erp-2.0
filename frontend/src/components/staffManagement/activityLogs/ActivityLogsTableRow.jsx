const ActivityLogsTableRow = ({ log }) => {
  return (
    <tr className="group transition-all duration-200 hover:bg-gradient-to-r hover:from-indigo-50/60 hover:to-cyan-50/40">
      <td className="px-8 py-4 font-mono text-sm text-outline">
        {log.id}
      </td>

      {/* Employee */}
      <td className="px-8 py-4">
        <div className="flex items-center gap-3">
          {log.avatar ? (
            <div className="h-10 w-10 shrink-0 overflow-hidden rounded-full bg-gradient-to-br from-indigo-100 to-cyan-100 p-0.5 ring-2 ring-indigo-100">
              <img
                src={log.avatar}
                alt={log.name}
                className="h-full w-full rounded-full object-cover"
              />
            </div>
          ) : (
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-cyan-500 text-sm font-semibold text-on-primary shadow-md shadow-indigo-200">
              {log.initials}
            </div>
          )}
          <div>
            <p className="text-sm font-semibold text-on-background">{log.name}</p>
            <p className="text-xs text-outline">{log.role}</p>
          </div>
        </div>
      </td>

      {/* Action */}
      <td className="px-8 py-4">
        <div className="flex items-center gap-2">
          <span className={`h-2 w-2 shrink-0 rounded-full ${log.dotClass} shadow-sm`} />
          <span className="text-sm text-on-surface-variant">{log.action}</span>
        </div>
      </td>

      {/* Module */}
      <td className="px-8 py-4">
        <span className="rounded-full bg-gradient-to-r from-slate-50 to-indigo-50/50 px-3 py-1 text-xs font-medium text-indigo-700 ring-1 ring-indigo-100">
          {log.module}
        </span>
      </td>

      {/* Timestamp */}
      <td className="px-8 py-4">
        <div className="font-mono text-sm text-on-surface-variant">
          {log.timestamp}
        </div>
      </td>

      {/* IP Address */}
      <td className="px-8 py-4 text-center">
        <span className="inline-flex items-center rounded-lg bg-surface-container-low px-2.5 py-1 font-mono text-xs font-medium text-on-surface-variant ring-1 ring-outline-variant">
          {log.ipAddress}
        </span>
      </td>
    </tr>
  );
};

export default ActivityLogsTableRow;