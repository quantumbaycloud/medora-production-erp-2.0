import { ChevronDown, Plus, Trash2, CheckCircle, AlertTriangle, Info } from "lucide-react";
import { Th, Td } from "./Shared";

export default function BatchEntryTab({
  receivedItems,
  currentBatchItemId,
  setCurrentBatchItemId,
  itemBatches,
  updateBatchValue,
  addBatchRow,
  removeBatchRow,
  calculateBatchTotal,
}) {
  const selectedItem = receivedItems.find((item) => item.id === currentBatchItemId);
  const batchTotal = selectedItem ? calculateBatchTotal(selectedItem.id) : 0;
  const batches = selectedItem ? itemBatches[selectedItem.id] || [] : [];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded border border-[#c2c6d3] p-6">
        <div className="flex flex-col md:flex-row md:items-end gap-4 mb-6">
          <div className="flex-1">
            <label className="block font-label-md text-[#121c2a] mb-1.5">Select Received Item</label>
            <div className="relative">
              <select
                value={currentBatchItemId || ""}
                onChange={(e) => setCurrentBatchItemId(parseInt(e.target.value) || null)}
                className="w-full bg-white border border-[#c2c6d3] rounded px-4 py-2.5 font-body-md focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none transition-all appearance-none text-[#121c2a]"
              >
                <option value="">Select an item to enter batches...</option>
                {receivedItems.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.name} ({item.batch || "No Single Batch"})
                  </option>
                ))}
              </select>
              <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#424751] pointer-events-none" />
            </div>
          </div>
          <div className="bg-[#f8f9ff] px-4 py-2.5 rounded border border-[#c2c6d3] flex flex-col min-w-[140px]">
            <span className="text-[10px] uppercase text-[#424751] font-bold tracking-wider">Total Received</span>
            <span className="text-xl font-bold text-[#121c2a]">{selectedItem?.received || "-"}</span>
          </div>
        </div>

        {selectedItem && (
          <div>
            <div className="overflow-x-auto mb-4">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="text-left border-b border-[#c2c6d3] font-label-md text-[#424751] uppercase tracking-wider text-[11px]">
                    <Th className="w-12">#</Th>
                    <Th>Batch Number</Th>
                    <Th className="w-48 text-right">Quantity</Th>
                    <Th className="w-16 text-center">Action</Th>
                  </tr>
                </thead>
                <tbody>
                  {batches.map((batch, idx) => (
                    <tr key={idx} className={`${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} border-b border-[#c2c6d3] hover:bg-[#eff4ff] transition-colors`}>
                      <Td className="text-[#424751]">{idx + 1}</Td>
                      <Td>
                        <input
                          type="text"
                          value={batch.batchNo}
                          onChange={(e) => updateBatchValue(selectedItem.id, idx, "batchNo", e.target.value)}
                          placeholder="Enter Batch #"
                          className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 font-body-md outline-none focus:border-[#004287] focus:ring-2 focus:ring-[#d6e3ff] text-[#121c2a]"
                        />
                      </Td>
                      <Td>
                        <input
                          type="number"
                          value={batch.qty}
                          onChange={(e) => updateBatchValue(selectedItem.id, idx, "qty", e.target.value)}
                          className="w-full text-right bg-white border border-[#c2c6d3] rounded px-3 py-2 font-body-md outline-none focus:border-[#004287] focus:ring-2 focus:ring-[#d6e3ff] text-[#121c2a]"
                        />
                      </Td>
                      <Td className="text-center">
                        <button onClick={() => removeBatchRow(selectedItem.id, idx)} className="text-[#424751] hover:text-[#ba1a1a] transition-colors">
                          <Trash2 size={16} />
                        </button>
                      </Td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="bg-[#f8f9ff]">
                    <td className="py-3 px-4" colSpan="2">
                      <button onClick={() => addBatchRow(selectedItem.id)} className="flex items-center gap-2 text-[#004287] font-bold text-label-md hover:underline">
                        <Plus size={16} />
                        Add Batch Row
                      </button>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex flex-col items-end">
                        <span className="text-[10px] text-[#424751] font-bold uppercase tracking-wider">Total Entered</span>
                        <span className="text-lg font-bold text-[#121c2a]">{batchTotal}</span>
                      </div>
                    </td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
            </div>
            <div
              className={`flex items-center gap-3 p-4 rounded border ${
                batchTotal === selectedItem.received
                  ? "bg-[#94f7b9] border-[#006d40] text-[#006d40]"
                  : batchTotal > selectedItem.received
                  ? "bg-[#ffdad6] border-[#ba1a1a] text-[#ba1a1a]"
                  : "bg-[#d6e3ff] border-[#004287] text-[#004287]"
              }`}
            >
              {batchTotal === selectedItem.received ? (
                <CheckCircle size={18} />
              ) : batchTotal > selectedItem.received ? (
                <AlertTriangle size={18} />
              ) : (
                <Info size={18} />
              )}
              <span className="font-label-md">
                {batchTotal === selectedItem.received
                  ? "All quantities accounted for. Batch entry complete."
                  : batchTotal > selectedItem.received
                  ? `Overage: Entered quantity (${batchTotal}) exceeds received quantity (${selectedItem.received}).`
                  : `Pending: ${selectedItem.received - batchTotal} more items to be assigned to batches.`}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
