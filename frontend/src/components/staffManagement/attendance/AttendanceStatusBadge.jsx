import { CheckCircle2, Clock4, XCircle } from "lucide-react";

const STATUS_STYLES = {
  Present: {
    badgeClass: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
    icon: CheckCircle2,
    iconClass: "text-secondary"
  },
  Late: {
    badgeClass: "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim",
    icon: Clock4,
    iconClass: "text-tertiary"
  },
  Absent: {
    badgeClass: "bg-error-container text-on-error-container ring-1 ring-error-container",
    icon: XCircle,
    iconClass: "text-error"
  }
};

const AttendanceStatusBadge = ({ status }) => {
  const style = STATUS_STYLES[status] || {
    badgeClass: "bg-surface-container-low text-on-surface-variant ring-1 ring-outline-variant",
    icon: null,
    iconClass: "text-outline"
  };
  const Icon = style.icon;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold ${style.badgeClass}`}
    >
      {Icon && <Icon size={13} className={style.iconClass} />}
      {status}
    </span>
  );
};

export default AttendanceStatusBadge;