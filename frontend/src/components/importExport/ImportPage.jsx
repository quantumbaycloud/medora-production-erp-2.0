import { useState } from "react";
import {
  Upload,
  Download,
  Table,
  History,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  CheckCircle,
  Package,
  Users,
  Truck,
  X,
} from "lucide-react";
import { Th, Td, StatusBadge } from "./Shared";
import { tabData, importHistory } from "../../data/importExport/data";
import erpApi from "../../services/erpApi";

export default function ImportPage({ onToast }) {
  const [activeSubTab, setActiveSubTab] = useState("medicines");
  const [isUploaded, setIsUploaded] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [importing, setImporting] = useState(false);

  const getData = () => tabData[activeSubTab];

  const handleUpload = (event) => {
    const file = event.target?.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    setIsUploaded(true);
  };
  const handleResetUpload = () => setIsUploaded(false);

  const handleFixErrors = () => {
    const data = getData();
    const rowEl = document.getElementById(`preview-row-${data.errorRowIdx}`);
    if (rowEl) {
      rowEl.classList.add("animate-pulse");
      rowEl.style.backgroundColor = "#ffdad6";
      setTimeout(() => {
        rowEl.classList.remove("animate-pulse");
        rowEl.style.backgroundColor = "";
      }, 2000);
    }
  };

  const handleImportAnyway = async () => {
    if (activeSubTab !== "medicines" || !selectedFile) {
      onToast?.({ title: "Import unavailable", message: "Only medicine CSV import is currently supported by the ERP API.", icon: AlertCircle });
      return;
    }
    setImporting(true);
    try {
      const { data } = await erpApi.importMedicines(selectedFile);
      onToast?.({ title: "Import complete", message: `${data.successful || 0} rows imported; ${data.failed || 0} failed.`, icon: CheckCircle });
      setIsUploaded(false); setSelectedFile(null);
    } catch (error) {
      onToast?.({ title: "Import failed", message: error?.response?.data?.detail || error.message || "Import failed", icon: AlertCircle });
    } finally { setImporting(false); }
  };

  const handleDownloadTemplate = () => {
    const data = getData();
    let csv = data.headers.join(",") + "\n";
    data.rows.slice(0, 2).forEach((row) => {
      csv += row.slice(0, data.headers.length).join(",") + "\n";
    });
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `medorax_${activeSubTab}_template.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const renderPreviewTable = () => {
    const data = getData();
    return (
      <table className="w-full text-left text-sm whitespace-nowrap">
        <thead className="bg-[#eff4ff] text-[#121c2a] font-bold">
          <tr>
            {data.headers.map((h, i) => (
              <Th key={i}>{h}</Th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-[#c2c6d3] text-[#424751]">
          {data.rows.map((row, idx) => {
            const isError = idx === data.errorRowIdx;
            return (
              <tr
                key={idx}
                id={`preview-row-${idx}`}
                className={`transition-colors ${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} ${
                  isError ? "border-l-2 border-[#ba1a1a]" : ""
                } hover:bg-[#eff4ff]`}
              >
                {row.slice(0, data.headers.length).map((cell, cellIdx) => {
                  // Only show error icon on the first cell of the error row
                  const isErrorCell = isError && cellIdx === 0;
                  return (
                    <Td key={cellIdx} isError={isErrorCell}>
                      {cell}
                    </Td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Sub-tabs & Actions */}
      <div className="bg-white rounded border border-[#c2c6d3] p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="flex gap-2 bg-transparent">
          {[
            { key: "medicines", label: "Medicines", icon: Package },
            { key: "customers", label: "Customers", icon: Users },
            { key: "suppliers", label: "Suppliers", icon: Truck },
          ].map((s) => {
            const Icon = s.icon;
            const isActive = activeSubTab === s.key;
            return (
              <button
                key={s.key}
                onClick={() => setActiveSubTab(s.key)}
                className={`pb-2 px-3 text-sm font-medium relative transition-colors flex items-center gap-1.5 ${
                  isActive ? "text-[#004287] font-bold" : "text-[#424751] hover:text-[#121c2a]"
                }`}
              >
                <Icon size={16} />
                {s.label}
                {isActive && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#004287]"></div>
                )}
              </button>
            );
          })}
        </div>
        <button
          onClick={handleDownloadTemplate}
          className="px-4 py-1.5 text-sm font-medium rounded transition flex items-center gap-2 border border-[#004287] text-[#004287] hover:bg-[#eff4ff]"
        >
          <Download size={16} />
          Template
        </button>
      </div>

      {!isUploaded ? (
        <div
          className="border-2 border-dashed border-[#c2c6d3] rounded p-12 text-center bg-white transition-colors hover:border-[#004287] cursor-pointer flex flex-col items-center justify-center min-h-75"
          onClick={() => document.getElementById("erp-import-file")?.click()}
        >
          <input id="erp-import-file" type="file" accept=".csv,text/csv" className="hidden" onChange={handleUpload} />
          <Upload size={48} className="text-[#004287] mb-4 opacity-60" />
          <h3 className="font-headline-md text-[#121c2a] mb-2">Drag &amp; Drop file to import</h3>
          <p className="text-[#424751] text-sm mb-6">Supported formats: .csv, .xlsx (Max 50MB)</p>
          <button className="px-6 py-2 bg-white border border-[#c2c6d3] rounded font-medium text-[#004287] hover:bg-[#f8f9ff] transition">
            Browse File
          </button>
        </div>
      ) : (
        <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
          <div className="p-4 border-b border-[#c2c6d3] flex justify-between items-center bg-[#eff4ff]">
            <h3 className="font-semibold text-[#121c2a] flex items-center gap-2">
              <Table size={18} className="text-[#004287]" />
              Data Preview (<span className="font-normal">{activeSubTab.charAt(0).toUpperCase() + activeSubTab.slice(1)}.csv</span>)
            </h3>
            <button onClick={handleResetUpload} className="text-[#424751] hover:text-[#121c2a] transition">
              <X size={18} />
            </button>
          </div>
          <div className="overflow-x-auto">{renderPreviewTable()}</div>
          <div className="p-4 bg-[#eff4ff] border-t border-[#c2c6d3] flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="flex items-center gap-2 text-sm">
              <span className="px-2 py-1 bg-[#d6e3ff] rounded text-[#004287] font-medium">24 rows ready</span>
              <span className="text-[#424751]">•</span>
              <span className="px-2 py-1 bg-[#ffdad6] text-[#ba1a1a] rounded font-medium flex items-center gap-1">
                <AlertCircle size={14} />
                1 error found
              </span>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleFixErrors}
                className="px-4 py-2 text-[#ba1a1a] font-medium border border-[#ffdad6] rounded hover:bg-[#ffdad6] transition text-sm"
              >
                Fix Errors
              </button>
              <button
                onClick={handleImportAnyway} disabled={importing}
                className="px-4 py-2 bg-[#004287] text-white font-medium rounded hover:bg-[#235eac] transition text-sm"
              >
                Import Anyway
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white rounded border border-[#c2c6d3]">
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="w-full p-4 flex justify-between items-center bg-[#eff4ff] rounded-t hover:bg-[#d6e3ff] transition"
        >
          <h3 className="font-semibold text-[#121c2a] flex items-center gap-2">
            <History size={18} className="text-[#004287]" />
            Import History
          </h3>
          {showHistory ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>
        {showHistory && (
          <div className="border-t border-[#c2c6d3] overflow-x-auto">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-[#eff4ff] text-[#121c2a] font-bold">
                <tr>
                  <Th>Date</Th>
                  <Th>File Name</Th>
                  <Th>Type</Th>
                  <Th className="text-right">Rows Added</Th>
                  <Th className="text-center">Status</Th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#c2c6d3] text-[#424751]">
                {importHistory.map((item, idx) => (
                  <tr key={idx} className={`${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} hover:bg-[#eff4ff] transition-colors`}>
                    <Td>{item.date}</Td>
                    <Td className="font-medium text-[#121c2a]">{item.file}</Td>
                    <Td>{item.type}</Td>
                    <Td className="text-right">{item.rows}</Td>
                    <td className="py-3 px-4 text-center">
                      <StatusBadge status={item.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
