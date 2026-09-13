import { X, Save, User, Mail, Phone, Calendar, MapPin, FileText, Shield, Stethoscope } from "lucide-react";

const ROLES = ["Doctor", "Nurse", "Administrator", "Technician"];
const DEPARTMENTS = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Radiology", "Laboratory", "Emergency", "Administration"];
const STATUS_OPTIONS = ["Active", "On Leave", "Inactive"];

const INPUT_CLASSES =
  "w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface-variant placeholder:text-outline transition focus:border-primary focus:bg-surface-container-lowest focus:outline-none focus:ring-2 focus:ring-primary-fixed";

const StaffModal = ({
  isOpen,
  onClose,
  title,
  subtitle,
  onSubmit,
  formData,
  setFormData,
  submitLabel = "Save Changes"
}) => {
  if (!isOpen) return null;

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-inverse-surface/50 p-4">
      <div className="relative w-full max-w-3xl rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-outline-variant px-6 py-5">
          <div>
            <h2 className="text-xl font-bold text-on-background">{title}</h2>
            <p className="mt-0.5 text-sm text-on-surface-variant">{subtitle}</p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-on-surface-variant transition hover:bg-surface-container hover:text-on-surface-variant"
          >
            <X size={20} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={onSubmit} className="p-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            {/* Name */}
            <div className="sm:col-span-2">
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <User size={14} className="text-primary" />
                Full Name
              </label>
              <input
                type="text"
                placeholder="Enter full name"
                value={formData.name || ""}
                onChange={(e) => handleChange("name", e.target.value)}
                className={INPUT_CLASSES}
                required
              />
            </div>

            {/* Staff Code */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <FileText size={14} className="text-primary" />
                Staff Code
              </label>
              <input
                type="text"
                placeholder="e.g. STF-1001"
                value={formData.code || ""}
                onChange={(e) => handleChange("code", e.target.value)}
                className={INPUT_CLASSES}
                required
              />
            </div>

            {/* Role */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Shield size={14} className="text-primary" />
                Role
              </label>
              <select
                value={formData.role || "Doctor"}
                onChange={(e) => handleChange("role", e.target.value)}
                className={INPUT_CLASSES}
              >
                {ROLES.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            </div>

            {/* Email */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Mail size={14} className="text-primary" />
                Email
              </label>
              <input
                type="email"
                placeholder="name@hospital.com"
                value={formData.email || ""}
                onChange={(e) => handleChange("email", e.target.value)}
                className={INPUT_CLASSES}
                required
              />
            </div>

            {/* Phone */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Phone size={14} className="text-primary" />
                Phone
              </label>
              <input
                type="tel"
                placeholder="+1 (555) 123-4567"
                value={formData.phone || ""}
                onChange={(e) => handleChange("phone", e.target.value)}
                className={INPUT_CLASSES}
                required
              />
            </div>

            {/* Department */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Stethoscope size={14} className="text-primary" />
                Department
              </label>
              <select
                value={formData.department || "Cardiology"}
                onChange={(e) => handleChange("department", e.target.value)}
                className={INPUT_CLASSES}
              >
                {DEPARTMENTS.map((dept) => (
                  <option key={dept} value={dept}>
                    {dept}
                  </option>
                ))}
              </select>
            </div>

            {/* License */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Shield size={14} className="text-primary" />
                License Number
              </label>
              <input
                type="text"
                placeholder="e.g. MD-12345"
                value={formData.license || ""}
                onChange={(e) => handleChange("license", e.target.value)}
                className={INPUT_CLASSES}
                required
              />
            </div>

            {/* Status */}
            <div>
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <Calendar size={14} className="text-primary" />
                Status
              </label>
              <select
                value={formData.status || "Active"}
                onChange={(e) => handleChange("status", e.target.value)}
                className={INPUT_CLASSES}
              >
                {STATUS_OPTIONS.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>

            {/* Address */}
            <div className="sm:col-span-2">
              <label className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-on-surface-variant">
                <MapPin size={14} className="text-primary" />
                Address
              </label>
              <input
                type="text"
                placeholder="Enter full address"
                value={formData.address || ""}
                onChange={(e) => handleChange("address", e.target.value)}
                className={INPUT_CLASSES}
              />
            </div>
          </div>

          {/* Actions */}
          <div className="mt-8 flex items-center justify-end gap-3 border-t border-outline-variant pt-6">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-outline-variant bg-surface-container-lowest px-5 py-2.5 text-sm font-semibold text-on-surface-variant transition hover:bg-surface-container-low"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-on-primary shadow-md shadow-primary-fixed/50 transition hover:opacity-95 hover:shadow-lg"
            >
              <Save size={16} />
              <span>{submitLabel}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StaffModal;
