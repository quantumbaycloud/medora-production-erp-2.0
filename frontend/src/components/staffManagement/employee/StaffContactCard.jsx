import {
  Mail,
  Phone,
  MapPin,
  Calendar,
  Shield,
  Stethoscope,
  User
} from "lucide-react";

const StaffContactCard = ({ staff }) => {
  const contactItems = [
    {
      icon: User,
      label: "Full Name",
      value: staff.name,
      iconColor: "text-primary"
    },
    {
      icon: Mail,
      label: "Email Address",
      value: staff.email,
      iconColor: "text-primary"
    },
    {
      icon: Phone,
      label: "Phone Number",
      value: staff.phone,
      iconColor: "text-primary"
    },
    {
      icon: Stethoscope,
      label: "Department",
      value: staff.department,
      iconColor: "text-secondary"
    },
    {
      icon: Shield,
      label: "Role",
      value: staff.role,
      iconColor: "text-violet-500"
    },
    {
      icon: Calendar,
      label: "License Number",
      value: staff.license,
      iconColor: "text-tertiary"
    },
    {
      icon: MapPin,
      label: "Address",
      value: staff.address,
      iconColor: "text-on-surface-variant"
    }
  ];

  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="border-b border-outline-variant px-6 py-5">
        <h2 className="text-base font-bold text-on-background">
          Contact Information
        </h2>
        <p className="mt-0.5 text-sm text-on-surface-variant">
          Primary contact details for {staff.name}
        </p>
      </div>

      <div className="p-6">
        <div className="space-y-4">
          {contactItems.map((item, index) => {
            const Icon = item.icon;

            return (
              <div key={index} className="flex items-start gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-surface-container-low ring-1 ring-slate-100">
                  <Icon size={14} className={item.iconColor} />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-semibold uppercase tracking-wider text-outline">
                    {item.label}
                  </p>
                  <p className="mt-0.5 text-sm text-on-surface-variant break-words">
                    {item.value}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default StaffContactCard;
