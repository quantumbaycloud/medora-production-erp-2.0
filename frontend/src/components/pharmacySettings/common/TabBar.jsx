const TabBar = ({ tabs, activeTab, onChange }) => {
  return (
    <div className="mb-8 flex items-center gap-6 overflow-x-auto border-b border-outline-variant">
      {tabs.map((tab) => {
        const isActive = tab.id === activeTab;

        return (
          <button
            key={tab.id}
            type="button"
            onClick={() => onChange(tab.id)}
            aria-current={isActive ? "page" : undefined}
            className={`whitespace-nowrap px-2 pb-4 pt-1 text-sm font-bold uppercase tracking-wide transition-colors duration-150 ${
              isActive
                ? "border-b-2 border-primary text-primary"
                : "border-b-2 border-transparent text-on-surface-variant hover:text-primary"
            }`}
          >
            {tab.label}
          </button>
        );
      })}
    </div>
  );
};

export default TabBar;