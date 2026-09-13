const inputClasses =
  "w-full rounded-xl border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-sm text-on-surface transition-all duration-200 placeholder:text-outline focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10";

const FormField = ({ label, type = "text", options, ...inputProps }) => {
  const fieldId = `field-${label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;

  return (
    <div className="flex flex-col gap-1.5">
      <label
        htmlFor={fieldId}
        className="text-xs font-bold uppercase tracking-wider text-on-surface-variant"
      >
        {label}
      </label>

      {type === "select" ? (
        <select id={fieldId} className={inputClasses} {...inputProps}>
          {options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      ) : (
        <input id={fieldId} type={type} className={inputClasses} {...inputProps} />
      )}
    </div>
  );
};

export default FormField;