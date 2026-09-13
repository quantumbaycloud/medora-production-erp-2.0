const variantStyles = {
  success: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
  warning: "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim",
  danger: "bg-error-container text-on-error-container ring-1 ring-error-container",
  info: "bg-primary-fixed text-primary ring-1 ring-primary-fixed-dim",
  neutral: "bg-surface-container text-on-surface-variant ring-1 ring-outline-variant",
};

const StatusBadge = ({ status, variant = "neutral", className = "" }) => {
  return (
    <span
      className={`inline-flex items-center whitespace-nowrap rounded-full px-3 py-1 text-[11px] font-bold uppercase tracking-wide ${variantStyles[variant]} ${className}`}
    >
      {status}
    </span>
  );
};

export default StatusBadge;
