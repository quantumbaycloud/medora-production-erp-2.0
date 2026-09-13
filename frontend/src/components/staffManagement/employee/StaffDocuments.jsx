import { FileText, Download, ExternalLink } from "lucide-react";

const DOCUMENT_STATUS_STYLES = {
  Valid: "bg-secondary-container text-on-secondary-fixed-variant ring-1 ring-secondary-fixed-dim",
  Expired: "bg-error-container text-on-error-container ring-1 ring-error-container",
  "Pending": "bg-tertiary-fixed text-on-tertiary-fixed-variant ring-1 ring-tertiary-fixed-dim"
};

const StaffDocuments = ({ staff }) => {
  const documents = [
    {
      id: 1,
      name: "Medical License",
      type: "PDF",
      date: "2025-03-15",
      status: "Valid",
      file: "license_md_1029.pdf"
    },
    {
      id: 2,
      name: "Board Certification",
      type: "PDF",
      date: "2024-11-20",
      status: "Valid",
      file: "cert_board_2024.pdf"
    },
    {
      id: 3,
      name: "BLS Certification",
      type: "PDF",
      date: "2023-08-10",
      status: "Expired",
      file: "bls_cert_2023.pdf"
    },
    {
      id: 4,
      name: "Malpractice Insurance",
      type: "PDF",
      date: "2025-01-05",
      status: "Valid",
      file: "insurance_2025.pdf"
    }
  ];

  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="flex items-center justify-between border-b border-outline-variant px-6 py-5">
        <div>
          <h2 className="text-base font-bold text-on-background">
            Staff Documents
          </h2>
          <p className="mt-0.5 text-sm text-on-surface-variant">
            Certifications and credentials for {staff.name}
          </p>
        </div>

        <button className="inline-flex items-center gap-1.5 rounded-lg border border-outline-variant bg-surface-container-low px-3 py-1.5 text-xs font-semibold text-on-surface-variant transition hover:bg-surface-container hover:text-on-background">
          <FileText size={14} />
          <span>Upload</span>
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-surface-container-low">
            <tr className="text-xs text-on-surface-variant">
              <th className="px-6 py-3.5 text-left font-semibold">Document</th>
              <th className="px-6 py-3.5 text-left font-semibold">Type</th>
              <th className="px-6 py-3.5 text-left font-semibold">Date</th>
              <th className="px-6 py-3.5 text-center font-semibold">Status</th>
              <th className="px-6 py-3.5 text-right font-semibold">Action</th>
            </tr>
          </thead>

          <tbody>
            {documents.map((doc) => (
              <tr
                key={doc.id}
                className="group border-b border-slate-100 transition-colors last:border-b-0 hover:bg-[#F8FCFF]/60"
              >
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-surface-container">
                      <FileText size={18} className="text-on-surface-variant" />
                    </div>
                    <div>
                      <p className="font-semibold text-on-background">
                        {doc.name}
                      </p>
                      <p className="font-mono text-xs text-outline">
                        {doc.file}
                      </p>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-on-surface-variant">{doc.type}</td>
                <td className="px-6 py-4 text-sm text-on-surface-variant">{doc.date}</td>
                <td className="px-6 py-4 text-center">
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      DOCUMENT_STATUS_STYLES[doc.status] ||
                      DOCUMENT_STATUS_STYLES.Pending
                    }`}
                  >
                    {doc.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <button className="rounded-lg p-1.5 text-on-surface-variant transition hover:bg-surface-container hover:text-on-surface-variant">
                      <Download size={14} />
                    </button>
                    <button className="rounded-lg p-1.5 text-on-surface-variant transition hover:bg-surface-container hover:text-on-surface-variant">
                      <ExternalLink size={14} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StaffDocuments;
