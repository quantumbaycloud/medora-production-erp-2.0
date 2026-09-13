
export default function OrderDetailsSection({
  poNumber,
  supplier,
  setSupplier,
  location,
  setLocation,
  poDate,
  setPoDate,
  deliveryDate,
  setDeliveryDate,
  refNumber,
  setRefNumber,
  supplierOptions = [],
}) {

  return (
    <div className="bg-white rounded border border-[#c2c6d3] p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">PO Number</label>
          <input
            type="text"
            value={poNumber}
            readOnly
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded bg-[#f8f9ff] text-[#121c2a]"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">Supplier *</label>
          <select
            value={supplier}
            onChange={(e) => setSupplier(e.target.value)}
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
          >
            <option value="">Select Supplier</option>
            {supplierOptions.map((s) => (
              <option key={s.id || s.value || s} value={s.id || s.value || s}>{s.name || s.label || s}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">Location</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">PO Date</label>
          <input
            type="date"
            value={poDate}
            onChange={(e) => setPoDate(e.target.value)}
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">Delivery Date</label>
          <input
            type="date"
            value={deliveryDate}
            onChange={(e) => setDeliveryDate(e.target.value)}
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#424751] mb-1">Reference Number</label>
          <input
            type="text"
            value={refNumber}
            onChange={(e) => setRefNumber(e.target.value)}
            placeholder="Optional"
            className="w-full px-3 py-2 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] text-[#121c2a]"
          />
        </div>
      </div>
    </div>
  );
}
