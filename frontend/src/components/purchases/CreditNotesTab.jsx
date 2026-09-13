import { Receipt, CloudUpload } from "lucide-react";
import { Th, Td } from "./Shared";
import { creditNotes } from "../../data/purchases/data";

export default function CreditNotesTab({
  creditNoteNumber,
  setCreditNoteNumber,
  creditNoteAmount,
  setCreditNoteAmount,
}) {
  return (
    <div className="space-y-6 pb-20">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded border border-[#c2c6d3]">
          <h3 className="font-semibold text-[#121c2a] mb-4 pb-2 border-b border-[#c2c6d3] flex items-center gap-2">
            <Receipt size={18} className="text-[#004287]" />
            Record New Credit Note
          </h3>
          <div className="space-y-4">
            <div className="flex flex-col gap-1.5">
              <label className="font-label-md text-[#121c2a]">Credit Note Number *</label>
              <input
                type="text"
                value={creditNoteNumber}
                onChange={(e) => setCreditNoteNumber(e.target.value)}
                placeholder="Enter CN Number"
                className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 font-body-md focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none text-[#121c2a]"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="font-label-md text-[#121c2a]">Amount (₹) *</label>
              <input
                type="number"
                value={creditNoteAmount}
                onChange={(e) => setCreditNoteAmount(e.target.value)}
                placeholder="0.00"
                className="w-full bg-white border border-[#c2c6d3] rounded px-3 py-2 font-body-md focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none text-[#121c2a]"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="font-label-md text-[#121c2a]">Upload Document</label>
              <div className="border-2 border-dashed border-[#c2c6d3] rounded p-6 text-center hover:bg-[#eff4ff] transition-colors cursor-pointer">
                <CloudUpload size={36} className="text-[#424751] mx-auto mb-2" />
                <p className="font-body-md text-[#424751]">
                  Drag &amp; Drop or <span className="text-[#004287] font-medium">Browse</span>
                </p>
              </div>
            </div>
            <button className="w-full bg-[#eff4ff] text-[#424751] font-medium py-2 rounded hover:bg-[#d6e3ff] transition-colors font-label-md">
              Add Credit Note
            </button>
          </div>
        </div>
        <div className="bg-white p-6 rounded border border-[#c2c6d3]">
          <h3 className="font-semibold text-[#121c2a] mb-4 pb-2 border-b border-[#c2c6d3]">Credit Note History</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#eff4ff] font-label-md text-[#121c2a] border-b border-[#c2c6d3] uppercase tracking-wider text-[11px]">
                  <Th>CN Number</Th>
                  <Th>Date</Th>
                  <Th className="text-right">Amount</Th>
                  <Th className="text-center">Status</Th>
                </tr>
              </thead>
              <tbody className="font-body-md text-[#424751] divide-y divide-[#c2c6d3]">
                {creditNotes.map((cn, idx) => (
                  <tr key={cn.number} className={`${idx % 2 === 0 ? "bg-white" : "bg-[#f8f9ff]"} hover:bg-[#eff4ff] transition-colors`}>
                    <Td className="font-medium text-[#121c2a]">{cn.number}</Td>
                    <Td className="text-[#424751]">{cn.date}</Td>
                    <Td className="text-right font-medium text-[#121c2a]">₹{cn.amount.toFixed(2)}</Td>
                    <Td className="text-center">
                      <span
                        className={`inline-flex px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                          cn.status === "APPLIED"
                            ? "bg-[#94f7b9] text-[#006d40] border border-[#006d40]"
                            : "bg-[#ffdad6] text-[#ba1a1a] border border-[#ba1a1a]"
                        }`}
                      >
                        {cn.status}
                      </span>
                    </Td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
