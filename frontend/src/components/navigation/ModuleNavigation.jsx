import { NavLink } from "react-router-dom";

const ModuleNavigation = ({ title, description, items }) => {
  return (
    <section className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="border-b border-outline-variant px-5 py-4 md:px-6">
        <h1 className="text-xl font-bold text-on-background md:text-2xl">{title}</h1>
        <p className="mt-1 text-sm text-on-surface-variant">{description}</p>
      </div>

      <nav aria-label={`${title} navigation`} className="overflow-x-auto">
        <div className="flex min-w-max gap-1 px-3 py-2 md:px-4">
          {items.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-primary text-on-primary shadow-sm"
                    : "text-on-surface-variant hover:bg-surface-container-low hover:text-primary"
                }`
              }
            >
              <Icon size={17} strokeWidth={2.2} />
              <span>{label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </section>
  );
};

export default ModuleNavigation;
