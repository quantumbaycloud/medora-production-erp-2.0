import { useState } from "react";
import { Upload, Download } from "lucide-react";
import { Toast } from "../../components/importExport/Shared";
import ImportPage from "../../components/importExport/ImportPage";
import ExportPage from "../../components/importExport/ExportPage";

export default function ImportExportPage() {
  const [activeTab, setActiveTab] = useState("import");
  const [toast, setToast] = useState(null);

  const showToast = (config) => {
    setToast(config);
    setTimeout(() => setToast(null), 3000);
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#f8f9ff]">
      {toast && (
        <Toast title={toast.title} message={toast.message} icon={toast.icon} onClose={() => setToast(null)} />
      )}

      <main className="flex-1 overflow-y-auto p-6 space-y-6 pt-0">
        <div className="bg-white border-b border-[#c2c6d3] sticky top-0 z-20 mt-4">
          <div className="flex overflow-x-auto no-scrollbar gap-8 py-2 whitespace-nowrap px-6">
            <div className="flex flex-col gap-2 overflow-y-hidden">
              <span className="text-[12px] font-bold text-[#004287] uppercase tracking-wider opacity-60 px-1">
                Data Management
              </span>
              <div className="flex gap-4 pb-2">
                {[
                  { key: "import", label: "Import", icon: Upload },
                  { key: "export", label: "Export", icon: Download },
                ].map((t) => {
                  const Icon = t.icon;
                  return (
                    <button
                      key={t.key}
                      onClick={() => setActiveTab(t.key)}
                      className={`text-[16px] text-[#004287] relative px-1 cursor-pointer transition-opacity flex items-center gap-1.5 ${
                        activeTab === t.key ? "font-bold opacity-100" : "opacity-80 hover:opacity-100"
                      }`}
                    >
                      <Icon size={16} />
                      {t.label}
                      <div
                        className={`absolute -bottom-2.5 left-0 right-0 h-1 rounded-t-full ${
                          activeTab === t.key ? "bg-[#004287]" : "hidden"
                        }`}
                      ></div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {activeTab === "import" && <ImportPage onToast={showToast} />}
        {activeTab === "export" && <ExportPage onToast={showToast} />}
      </main>
    </div>
  );
}
