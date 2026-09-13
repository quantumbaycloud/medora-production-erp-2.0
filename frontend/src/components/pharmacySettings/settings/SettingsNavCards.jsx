import { ArrowRight, Building2, Check, Store } from "lucide-react";

const navCards = [
  {
    id: "profile",
    title: "Pharmacy Profile",
    description: "Manage pharmacy business information and branding.",
    icon: Store,
  },
  {
    id: "branch",
    title: "Branch Management",
    description: "Manage all pharmacy branches and local stock nodes.",
    icon: Building2,
  },
];

const SettingsNavCards = ({ activeSection, onSelect }) => {
  return (
    <section className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-2">
      {navCards.map(({ id, title, description, icon: Icon }) => {
        const isActive = activeSection === id;

        return (
          <button
            key={id}
            type="button"
            onClick={() => onSelect(id)}
            aria-pressed={isActive}
            className={`group flex items-start gap-4 rounded-xl border bg-surface-container-lowest p-6 text-left shadow-sm transition-all hover:shadow-md ${
              isActive ? "border-primary ring-1 ring-primary" : "border-outline-variant"
            }`}
          >
            <span
              className={`rounded-xl p-3 transition-colors ${
                isActive ? "bg-primary/10 text-primary" : "bg-surface-container-low text-on-surface-variant group-hover:bg-primary/10 group-hover:text-primary"
              }`}
            >
              <Icon size={28} />
            </span>

            <span className="flex-1">
              <span className="block text-lg font-semibold text-on-background">{title}</span>
              <span className="mt-1 block text-sm text-on-surface-variant">{description}</span>
            </span>

            {isActive ? (
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-on-primary">
                <Check size={14} />
              </span>
            ) : (
              <ArrowRight size={20} className="text-primary opacity-0 transition-opacity group-hover:opacity-100" />
            )}
          </button>
        );
      })}
    </section>
  );
};

export default SettingsNavCards;