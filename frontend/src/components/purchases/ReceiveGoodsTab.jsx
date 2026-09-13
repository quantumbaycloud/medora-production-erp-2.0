import { ChevronDown, Plus, Package, FileText } from "lucide-react";
import { Th, Td, Pagination } from "./Shared";
import { poOptions, purchaseData } from "../../data/purchases/data";
import { supplierData } from "../../data/reports/mockData";

export default function ReceiveGoodsTab({
  selectedPO,
  setSelectedPO,
  invoiceNo,
  setInvoiceNo,
  invoiceDate,
  setInvoiceDate,
  receivedDate,
  setReceivedDate,
  receivedItems,
  updateItemData,
  notes,
  setNotes,
  totals,
  page,
  setPage,
}) {
  const selectedPurchase = purchaseData.find((p) => p.id === selectedPO || p.invoice_number === selectedPO);
  const selectedSupplier = supplierData.find((s) => s.id === selectedPurchase?.supplier_id);
  const totalRows = receivedItems.length;
  const totalPages = Math.max(Math.ceil(totalRows / 5), 1);
  const safePage = Math.min(Math.max(page, 1), totalPages);
  const pagedItems = receivedItems.slice((safePage - 1) * 5, safePage * 5);

  return (
    <div className="space-y-6 pb-20">
      <div className="bg-white rounded border border-[#c2c6d3] p-6">
        <div className="flex justify-between items-center mb-4 pb-3 border-b border-[#c2c6d3]">
          <h3 className="font-title-lg text-[#121c2a]">Receipt Details</h3>
          <span className="font-label-md text-[#004287] bg-[#d6e3ff] px-3 py-1 rounded font-bold">Receipt</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Select Purchase Order *</label>
            <div className="relative">
              <select
                value={selectedPO}
                onChange={(e) => setSelectedPO(e.target.value)}
                className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] appearance-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
              >
                <option disabled>Choose a PO...</option>
                {poOptions.map((po) => (
                  <option key={po} value={po}>
                    {po}
                  </option>
                ))}
              </select>
              <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#424751] pointer-events-none" />
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Supplier</label>
            <input
              type="text"
              value={selectedSupplier?.name || ""}
              readOnly
              className="w-full bg-[#f8f9ff] border border-[#c2c6d3] rounded px-3 py-2 text-[#424751] cursor-not-allowed font-body-md outline-none"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">PO Date</label>
            <input
              type="text"
              value={selectedPurchase?.invoice_date ? new Date(selectedPurchase.invoice_date).toLocaleDateString("en-IN") : "—"}
              readOnly
              className="w-full bg-[#f8f9ff] border border-[#c2c6d3] rounded px-3 py-2 text-[#424751] cursor-not-allowed font-body-md outline-none"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Invoice No. *</label>
            <input
              type="text"
              value={invoiceNo}
              onChange={(e) => setInvoiceNo(e.target.value)}
              placeholder="Enter Invoice Number"
              className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Invoice Date *</label>
            <input
              type="date"
              value={invoiceDate}
              onChange={(e) => setInvoiceDate(e.target.value)}
              className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Goods Received Date *</label>
            <input
              type="date"
              value={receivedDate}
              onChange={(e) => setReceivedDate(e.target.value)}
              className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
            />
          </div>
        </div>
      </div>

      <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden flex flex-col">
        <div className="p-4 border-b border-[#c2c6d3] flex justify-between items-center bg-[#eff4ff]">
          <h3 className="font-semibold text-[#121c2a] flex items-center gap-2">
            <Package size={18} className="text-[#004287]" />
            Received Items
          </h3>
          <button className="text-[#424751] font-label-md font-medium flex items-center gap-1 hover:text-[#004287] transition-colors border border-[#c2c6d3] px-3 py-1 rounded hover:bg-[#f8f9ff]">
            <Plus size={14} />
            Add Extra Item
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#eff4ff] font-label-md text-[#121c2a] border-b border-[#c2c6d3] uppercase tracking-wider text-[11px]">
                <Th>#</Th>
                <Th>Item Name</Th>
                <Th className="text-right">Ordered</Th>
                <Th className="text-right w-32">Received</Th>
                <Th className="w-40">Batch No.</Th>
                <Th className="w-40">Expiry Date</Th>
                <Th className="text-center">Status</Th>
              </tr>
            </thead>
            <tbody className="font-body-md text-[#424751] divide-y divide-[#c2c6d3]">
              {pagedItems.map((item, idx) => (
                <tr
                  key={item.id}
                  className={`${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} hover:bg-[#eff4ff] transition-colors`}
                >
                  <Td className="text-[#424751]">{(safePage - 1) * 5 + idx + 1}</Td>
                  <Td className="font-medium text-[#121c2a]">{item.name}</Td>
                  <Td className="text-right text-[#424751]">{item.ordered}</Td>
                  <Td>
                    <input
                      type="number"
                      min="0"
                      value={item.received}
                      onChange={(e) => updateItemData(item.id, "received", e.target.value)}
                      className="w-full text-right bg-white border border-[#c2c6d3] rounded p-1.5 focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none text-[#121c2a]"
                    />
                  </Td>
                  <Td>
                    <input
                      type="text"
                      value={item.batch}
                      onChange={(e) => updateItemData(item.id, "batch", e.target.value)}
                      placeholder="Batch No"
                      className="w-full bg-white border border-[#c2c6d3] rounded p-1.5 focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none text-[#121c2a]"
                    />
                  </Td>
                  <Td>
                    <input
                      type="month"
                      value={item.expiry}
                      onChange={(e) => updateItemData(item.id, "expiry", e.target.value)}
                      className="w-full bg-white border border-[#c2c6d3] rounded p-1.5 focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none text-[#121c2a]"
                    />
                  </Td>
                  <Td className="text-center">
                    <span className="inline-flex px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider bg-[#94f7b9] text-[#006d40] border border-[#006d40]">
                      COMPLETE
                    </span>
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination page={safePage} totalRows={totalRows} onPageChange={setPage} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded border border-[#c2c6d3] p-6">
          <h3 className="font-semibold text-[#121c2a] mb-3 flex items-center gap-2">
            <FileText size={18} className="text-[#004287]" />
            Delivery Notes
          </h3>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any remarks regarding damaged goods, delays, etc."
            className="w-full h-24 bg-white border border-[#c2c6d3] rounded p-3 font-body-md focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none resize-none text-[#121c2a]"
          />
        </div>
        <div className="bg-white rounded border border-[#c2c6d3] p-6 flex flex-col justify-center">
          <h3 className="font-semibold text-[#121c2a] mb-4 pb-2 border-b border-[#c2c6d3]">Summary</h3>
          <div className="flex justify-between items-center mb-3">
            <span className="font-body-md text-[#424751]">Total Ordered Qty:</span>
            <span className="font-label-md font-bold text-[#121c2a]">{totals.totalOrdered}</span>
          </div>
          <div className="flex justify-between items-center mb-4">
            <span className="font-body-md text-[#424751]">Total Received Qty:</span>
            <span className="font-label-md font-bold text-[#004287]">{totals.totalReceived}</span>
          </div>
          <div className="flex justify-between items-center pt-3 border-t border-[#c2c6d3]">
            <span className="font-body-md text-[#424751] font-medium">Variance:</span>
            <span className={`font-label-md font-bold ${totals.variance === 0 ? "text-[#006d40]" : "text-[#ba1a1a]"}`}>
              {totals.variance > 0 ? "+" : ""}
              {totals.variance}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
