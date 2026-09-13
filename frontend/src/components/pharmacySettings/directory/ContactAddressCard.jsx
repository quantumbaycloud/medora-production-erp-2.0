import { FileText, MapPin } from "lucide-react";
import { directorySummary } from "../../../data/pharmacySettings/pharmacySettingsData";

const ContactAddressCard = () => {
  const { contact } = directorySummary;

  return (
    <div className="flex flex-col rounded-2xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
      <div className="mb-4 flex-1 space-y-4">
        <div className="flex gap-3">
          <MapPin size={20} className="mt-1 shrink-0 text-primary" />
          <div>
            <p className="text-xs font-bold text-on-background">Registered Address</p>
            <p className="mt-0.5 text-sm text-on-surface-variant">{contact.address}</p>
          </div>
        </div>
        <div className="flex gap-3">
          <FileText size={20} className="shrink-0 text-primary" />
          <div>
            <p className="text-xs font-bold text-on-background">Website</p>
            <a
              href="#"
              className="mt-0.5 block text-sm font-medium text-primary hover:underline"
            >
              {contact.website}
            </a>
          </div>
        </div>
      </div>

      <div className="relative h-32 overflow-hidden rounded-xl border border-outline-variant bg-primary-fixed">
        <div className="absolute inset-0 flex items-center justify-center">
          <button
            type="button"
            className="rounded-full bg-surface-container-lowest px-3 py-1.5 text-[10px] font-bold text-on-background shadow-md transition-transform hover:scale-105"
          >
            Expand Map
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContactAddressCard;