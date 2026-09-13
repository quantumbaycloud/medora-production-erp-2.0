const toneClasses = {
  success: "cp-chip-success",
  warning: "cp-chip-warning",
  error: "cp-chip-error",
  info: "cp-chip-info",
  neutral: "cp-chip-neutral",
};

const StatusChip = ({ children, tone = "neutral" }) => {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide ${toneClasses[tone]}`}
    >
      {children}
    </span>
  );
};

export default StatusChip;