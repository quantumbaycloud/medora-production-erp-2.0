export default function NotesAndSummary({ notes, setNotes, totals }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <div className="bg-white rounded border border-[#c2c6d3] p-4">
          <h3 className="font-semibold text-[#121c2a] mb-2">Notes</h3>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any additional notes..."
            className="w-full h-24 p-3 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] resize-none text-[#121c2a]"
          />
        </div>
      </div>
      <div>
        <div className="bg-white rounded border border-[#c2c6d3] p-4 space-y-2">
          <h3 className="font-semibold text-[#121c2a] mb-4">Summary</h3>
          <div className="flex justify-between text-sm">
            <span className="text-[#424751]">Subtotal</span>
            <span className="font-medium text-[#121c2a]">₹{totals.subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-[#424751]">Tax Total</span>
            <span className="font-medium text-[#121c2a]">₹{totals.taxTotal.toFixed(2)}</span>
          </div>
          <div className="border-t border-[#c2c6d3] pt-2 mt-2">
            <div className="flex justify-between font-bold text-[#121c2a]">
              <span>Grand Total</span>
              <span>₹{totals.grandTotal.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
