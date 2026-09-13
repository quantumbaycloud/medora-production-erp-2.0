import { ChevronDown, Undo2 } from "lucide-react";
import { Th, Td, Pagination } from "./Shared";
import { returnReasons } from "../../data/purchases/data";

export default function PurchaseReturnTab({
  receivedItems,
  returnReason,
  setReturnReason,
  returnDate,
  setReturnDate,
  returnQuantities,
  updateReturnQuantity,
  estimatedCredit,
  page,
  setPage,
}) {
  const totalRows = receivedItems.length;
  const totalPages = Math.max(Math.ceil(totalRows / 5), 1);
  const safePage = Math.min(Math.max(page, 1), totalPages);
  const pagedItems = receivedItems.slice((safePage - 1) * 5, safePage * 5);

  return (
    <div className="space-y-6 pb-20">
      <div className="bg-white rounded border border-[#c2c6d3] p-6">
        <h3 className="font-semibold text-[#121c2a] mb-4 pb-2 border-b border-[#c2c6d3] flex items-center gap-2">
          <Undo2 size={18} className="text-[#004287]" />
          Return Details
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Reason for Return</label>
            <div className="relative">
              <select
                value={returnReason}
                onChange={(e) => setReturnReason(e.target.value)}
                className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] appearance-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
              >
                {returnReasons.map((reason) => (
                  <option key={reason} value={reason}>
                    {reason}
                  </option>
                ))}
              </select>
              <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#424751] pointer-events-none" />
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="font-label-md text-[#121c2a]">Return Date</label>
            <input
              type="date"
              value={returnDate}
              onChange={(e) => setReturnDate(e.target.value)}
              className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 text-[#121c2a] focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] font-body-md outline-none"
            />
          </div>
        </div>

        <h3 className="font-semibold text-[#121c2a] mb-4 pb-2 border-b border-[#c2c6d3]">Items to Return</h3>
        <div className="overflow-x-auto mb-6">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#eff4ff] font-label-md text-[#121c2a] border-b border-[#c2c6d3] uppercase tracking-wider text-[11px]">
                <Th>Item Name</Th>
                <Th>Batch No.</Th>
                <Th className="text-right">Received Qty</Th>
                <Th className="text-right w-32">Return Qty</Th>
                <Th className="text-center">Status</Th>
              </tr>
            </thead>
            <tbody className="font-body-md text-[#424751] divide-y divide-[#c2c6d3]">
              {pagedItems.map((item, idx) => {
                const returnQty = returnQuantities[item.id] || 0;
                const isReturning = returnQty > 0;
                return (
                  <tr key={item.id} className={`${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} hover:bg-[#eff4ff] transition-colors border-b border-[#c2c6d3]`}>
                    <Td className="font-medium text-[#121c2a]">{item.name}</Td>
                    <Td className="text-[#424751]">{item.batch}</Td>
                    <Td className="text-right text-[#424751]">{item.received}</Td>
                    <Td>
                      <input
                        type="number"
                        min="0"
                        max={item.received}
                        value={returnQty}
                        onChange={(e) => updateReturnQuantity(item.id, e.target.value)}
                        className="w-full text-right bg-white border border-[#c2c6d3] rounded p-1.5 outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
                      />
                    </Td>
                    <Td className="text-center">
                      <span
                        className={`inline-flex px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                          isReturning
                            ? "bg-[#ffdad6] text-[#ba1a1a] border border-[#ba1a1a]"
                            : "bg-[#f8f9ff] text-[#424751] border border-[#c2c6d3]"
                        }`}
                      >
                        {isReturning ? "RETURN" : "NO RETURN"}
                      </span>
                    </Td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <Pagination page={safePage} totalRows={totalRows} onPageChange={setPage} />
        <div className="bg-[#f8f9ff] p-4 rounded border border-[#c2c6d3] flex justify-between items-center">
          <span className="font-body-md text-[#424751] font-medium">Estimated Credit Amount</span>
          <span className="font-headline-md font-bold text-[#004287]">₹{estimatedCredit.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
