import { BadgeCheck } from "lucide-react";

const EmployeeIdInput = ({ value, onChange }) => {
  return (
    <div className="space-y-2">
      <label
        htmlFor="employee-id"
        className="ml-3 text-sm font-semibold text-on-background"
      >
        Enter Employee ID
      </label>
      <div className="relative group">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-outline transition-colors group-focus-within:text-primary">
          <BadgeCheck size={22} />
        </span>
        <input
          id="employee-id"
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="e.g. MX-8829"
          className="w-full rounded-xl border border-outline py-4 pl-12 pr-4 text-2xl font-medium tracking-wider outline-none transition-all focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
        />
      </div>
    </div>
  );
};

export default EmployeeIdInput;