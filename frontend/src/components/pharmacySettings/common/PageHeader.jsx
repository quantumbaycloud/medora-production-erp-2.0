const PageHeader = ({ title, description, actions }) => {
  return (
    <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-on-background">{title}</h2>
        {description && (
          <p className="mt-2 max-w-2xl text-sm text-on-surface-variant">{description}</p>
        )}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-3">{actions}</div>}
    </div>
  );
};

export default PageHeader;