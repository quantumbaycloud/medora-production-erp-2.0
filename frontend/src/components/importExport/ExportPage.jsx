import { useState } from "react";
import {
  FileSpreadsheet,
  FileText,
  Layers,
  Filter,
  ArrowRight,
  Package,
  Users,
  Truck,
  EyeOff,
  RefreshCw,
  CheckCircle,
} from "lucide-react";
import { exportColumns } from "../../data/importExport/data";
import erpApi from "../../services/erpApi";

export default function ExportPage({ onToast }) {
  const [isExporting, setIsExporting] = useState(false);
  const [entity, setEntity] = useState("medicines");
  const [format, setFormat] = useState("csv");
  const [selectedColumns, setSelectedColumns] = useState(
    exportColumns.map((c) => ({ name: c, checked: true }))
  );

  const toggleColumn = (index) => {
    setSelectedColumns((prev) =>
      prev.map((col, i) => (i === index ? { ...col, checked: !col.checked } : col))
    );
  };

  const toggleAllColumns = () => {
    const allChecked = selectedColumns.every((c) => c.checked);
    setSelectedColumns((prev) => prev.map((col) => ({ ...col, checked: !allChecked })));
  };

  const handleExport = async () => {
    setIsExporting(true);
    try {
      await erpApi.exportEntity(entity, format === "xlsx" ? "excel" : format);
      onToast?.({ title: "Export Complete", message: `${entity} export downloaded successfully.`, icon: CheckCircle });
    } catch (error) {
      onToast?.({ title: "Export Failed", message: error?.response?.data?.detail || error.message || "Export failed", icon: CheckCircle });
    } finally { setIsExporting(false); }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Configuration */}
        <div className="lg:col-span-2 space-y-6">
          {/* Data Type Selection */}
          <div className="bg-white rounded border border-[#c2c6d3] p-6">
            <h3 className="font-semibold text-[#121c2a] mb-4 flex items-center gap-2">
              <Layers size={18} className="text-[#004287]" />
              Select Data Type
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { key: "medicines", label: "Medicines Inventory", icon: Package },
                { key: "customers", label: "Customer Records", icon: Users },
                { key: "suppliers", label: "Supplier Directory", icon: Truck },
              ].map((type) => {
                const Icon = type.icon;
                return (
                  <label key={type.key} className="cursor-pointer">
                    <input
                      type="radio"
                      name="export-type"
                      checked={entity === type.key}
                      onChange={() => setEntity(type.key)}
                      className="peer sr-only"
                    />
                    <div className="p-4 rounded border-2 border-[#c2c6d3] peer-checked:border-[#004287] peer-checked:bg-[#d6e3ff] transition flex flex-col items-center text-center gap-2 hover:bg-[#f8f9ff]">
                      <Icon size={28} className="text-[#004287]" />
                      <span className="font-medium text-sm text-[#121c2a]">{type.label}</span>
                    </div>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="bg-white rounded border border-[#c2c6d3] p-6">
            <h3 className="font-semibold text-[#121c2a] mb-4 flex items-center gap-2">
              <Filter size={18} className="text-[#004287]" />
              Format &amp; Columns
            </h3>
            <div className="mb-6">
              <label className="block text-sm font-medium text-[#424751] mb-2">Export Format</label>
              <div className="flex gap-4 flex-wrap">
                {[
                  { key: "csv", label: "CSV (.csv)", icon: FileSpreadsheet },
                  { key: "xlsx", label: "Excel (.xlsx)", icon: FileSpreadsheet },
                  { key: "pdf", label: "PDF (.pdf)", icon: FileText },
                ].map((formatOption) => {
                  const Icon = formatOption.icon;
                  return (
                    <label key={formatOption.key} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="format"
                        checked={format === formatOption.key}
                        onChange={() => setFormat(formatOption.key)}
                        className="text-[#004287] focus:ring-[#004287] h-4 w-4"
                      />
                      <span className="text-sm text-[#121c2a] flex items-center gap-1">
                        <Icon size={14} />
                        {formatOption.label}
                      </span>
                    </label>
                  );
                })}
              </div>
            </div>
            <div className="border-t border-[#c2c6d3] pt-4">
              <div className="flex justify-between items-center mb-3">
                <label className="block text-sm font-medium text-[#424751]">Select Columns</label>
                <button onClick={toggleAllColumns} className="text-xs text-[#004287] font-medium hover:underline">
                  {selectedColumns.every((c) => c.checked) ? "Deselect All" : "Select All"}
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {selectedColumns.map((col, idx) => (
                  <label key={idx} className="flex items-center gap-2 text-sm text-[#424751] cursor-pointer hover:text-[#121c2a]">
                    <input
                      type="checkbox"
                      checked={col.checked}
                      onChange={() => toggleColumn(idx)}
                      className="text-[#004287] rounded focus:ring-[#004287]"
                    />
                    {col.name}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right: Summary */}
        <div className="space-y-6">
          <div className="bg-white rounded border border-[#c2c6d3] p-6 flex flex-col h-full">
            <h3 className="font-semibold text-[#121c2a] mb-4">Export Summary</h3>
            <div className="space-y-3 flex-1">
              <div className="flex justify-between text-sm pb-2 border-b border-[#c2c6d3]">
                <span className="text-[#424751]">Data Source</span>
                <span className="font-medium text-[#121c2a]">Medicines Inventory</span>
              </div>
              <div className="flex justify-between text-sm pb-2 border-b border-[#c2c6d3]">
                <span className="text-[#424751]">Columns Selected</span>
                <span className="font-medium text-[#121c2a]">
                  {selectedColumns.filter((c) => c.checked).length} of {selectedColumns.length}
                </span>
              </div>
              <div className="flex justify-between text-sm pb-2 border-b border-[#c2c6d3]">
                <span className="text-[#424751]">Est. Row Count</span>
                <span className="font-medium text-[#121c2a]">~15,420</span>
              </div>
              <div className="mt-4 relative rounded border border-[#c2c6d3] overflow-hidden bg-[#f8f9ff] h-24">
                <div className="absolute inset-0 bg-white/50 backdrop-blur-[2px] z-10 flex items-center justify-center">
                  <span className="text-xs font-medium text-[#424751] flex items-center gap-1">
                    <EyeOff size={14} />
                    Preview Blurred
                  </span>
                </div>
                <table className="w-full text-[8px] text-[#424751] opacity-50">
                  <tbody>
                    <tr className="border-b border-[#c2c6d3]">
                      <th className="p-1 text-[#424751]">SKU</th>
                      <th className="p-1 text-[#424751]">Name</th>
                      <th className="p-1 text-[#424751]">Cat</th>
                    </tr>
                    <tr>
                      <td className="p-1">M-01</td>
                      <td className="p-1">Data</td>
                      <td className="p-1">A</td>
                    </tr>
                    <tr>
                      <td className="p-1">M-02</td>
                      <td className="p-1">Data</td>
                      <td className="p-1">B</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <button
              onClick={handleExport}
              disabled={isExporting}
              className="mt-6 w-full py-3 bg-[#004287] text-white font-bold rounded hover:bg-[#235eac] transition-all flex items-center justify-center gap-2 disabled:opacity-70"
            >
              {isExporting ? (
                <>
                  <RefreshCw size={16} className="animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  Export Data Now
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
