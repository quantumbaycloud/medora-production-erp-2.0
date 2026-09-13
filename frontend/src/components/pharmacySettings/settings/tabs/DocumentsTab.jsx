import { Upload } from "lucide-react";
import StatusChip from "../../common/StatusChip";
import { pharmacyProfile } from "../../../../data/pharmacySettings/pharmacySettingsData";

const documentTone = {
  success: "success",
  warning: "warning",
};

const DocumentsTab = () => (
  <div>
    <div className="mb-6 flex items-center justify-between">
      <h4 className="text-lg font-semibold text-on-background">Pharmacy Documents</h4>
      <button
        type="button"
        className="flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-xs font-bold uppercase text-on-primary shadow-sm transition-colors hover:bg-primary-container"
      >
        <Upload size={14} />
        Upload New Document
      </button>
    </div>

    <div className="overflow-x-auto rounded-xl border border-outline-variant">
      <table className="w-full text-left">
        <thead className="cp-table-header">
          <tr>
            <th className="px-6 py-4">Document Name</th>
            <th className="px-6 py-4">Status</th>
            <th className="px-6 py-4">Last Uploaded</th>
            <th className="px-6 py-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant">
          {pharmacyProfile.documents.map((document) => (
            <tr key={document.name} className="cp-table-row-hover">
              <td className="px-6 py-4 font-semibold text-on-background">{document.name}</td>
              <td className="px-6 py-4">
                <StatusChip tone={documentTone[document.statusTone]}>
                  {document.status}
                </StatusChip>
              </td>
              <td className="px-6 py-4 text-sm text-on-surface-variant">
                {document.uploadedOn}
              </td>
              <td className="px-6 py-4 text-right">
                <button
                  type="button"
                  className="mr-4 text-xs font-bold text-primary hover:underline"
                >
                  View
                </button>
                <button
                  type="button"
                  className="text-xs font-bold text-on-surface-variant transition-colors hover:text-primary"
                >
                  Update
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default DocumentsTab;