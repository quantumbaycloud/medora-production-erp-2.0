import { useState } from "react";

const ToggleSwitch = ({ label, description, defaultEnabled = false }) => {
  const [enabled, setEnabled] = useState(defaultEnabled);

  return (
    <div className="flex items-center justify-between rounded-xl border border-outline-variant p-4">
      <div className="flex flex-col">
        <span className="font-semibold text-on-surface">{label}</span>
        {description && (
          <span className="text-xs text-on-surface-variant">{description}</span>
        )}
      </div>

      <button
        type="button"
        role="switch"
        aria-checked={enabled}
        aria-label={label}
        onClick={() => setEnabled((previous) => !previous)}
        className={`relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors duration-200 ${
          enabled ? "bg-primary" : "bg-outline-variant"
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform duration-200 ${
            enabled ? "translate-x-6" : "translate-x-1"
          }`}
        />
      </button>
    </div>
  );
};

export default ToggleSwitch;