// Shared KPI stat card used across all inventory pages
const StatCard = ({ title, value, subtitle, footerIcon, footerText, footerClass = "text-on-surface-variant" }) => {
  const FooterIcon = footerIcon;
  return (
    <div className="relative overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
      <div className="absolute inset-y-0 left-0 w-1 bg-primary" />
      <p className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
        {title}
      </p>
      <h3 className="mt-2 text-[28px] font-bold leading-9 text-on-background">
        {value}
      </h3>
      {(footerText || FooterIcon) && (
        <div className={`mt-4 flex items-center gap-1.5 text-xs font-medium ${footerClass}`}>
          {FooterIcon && <FooterIcon size={14} strokeWidth={2.5} />}
          <span>{footerText}</span>
        </div>
      )}
      {subtitle && (
        <p className="mt-4 text-xs text-outline">{subtitle}</p>
      )}
    </div>
  );
};

export default StatCard;
