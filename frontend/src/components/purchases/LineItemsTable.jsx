import { Trash2, Plus } from "lucide-react";
import { Th, Td } from "./Shared";

export default function LineItemsTable({
  items,
  updateItem,
  addItem,
  removeItem,
  calculateItemTotal,
}) {
  return (
    <div className="bg-white rounded border border-[#c2c6d3] overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#eff4ff] text-[#121c2a] font-bold">
              <Th className="w-8">#</Th>
              <Th>Product</Th>
              <Th className="min-w-[100px]">SKU</Th>
              <Th className="min-w-[80px]">Qty</Th>
              <Th className="min-w-[100px]">Unit</Th>
              <Th className="min-w-[100px]">Price</Th>
              <Th className="min-w-[80px]">Tax %</Th>
              <Th className="min-w-[120px] text-right">Total</Th>
              <Th className="w-10"></Th>
            </tr>
          </thead>
          <tbody className="text-[#424751]">
            {items.map((item, index) => (
              <tr key={item.id} className="border-b border-[#c2c6d3] hover:bg-[#f8f9ff]">
                <Td className="text-center">{index + 1}</Td>
                <Td>
                  <input
                    type="text"
                    value={item.product}
                    onChange={(e) => updateItem(item.id, "product", e.target.value)}
                    placeholder="Product name"
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] bg-white text-[#121c2a]"
                  />
                </Td>
                <Td>
                  <input
                    type="text"
                    value={item.sku}
                    readOnly
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded bg-[#f8f9ff] text-[#424751]"
                  />
                </Td>
                <Td>
                  <input
                    type="number"
                    value={item.qty}
                    onChange={(e) => updateItem(item.id, "qty", Number(e.target.value))}
                    min="1"
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] bg-white text-[#121c2a]"
                  />
                </Td>
                <Td>
                  <select
                    value={item.unit}
                    onChange={(e) => updateItem(item.id, "unit", e.target.value)}
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] bg-white text-[#121c2a]"
                  >
                    <option value="units">Units</option>
                    <option value="boxes">Boxes</option>
                    <option value="packs">Packs</option>
                  </select>
                </Td>
                <Td>
                  <input
                    type="number"
                    value={item.price}
                    onChange={(e) => updateItem(item.id, "price", Number(e.target.value))}
                    min="0"
                    step="0.01"
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] bg-white text-[#121c2a]"
                  />
                </Td>
                <Td>
                  <input
                    type="number"
                    value={item.tax}
                    onChange={(e) => updateItem(item.id, "tax", Number(e.target.value))}
                    min="0"
                    max="100"
                    step="0.01"
                    className="w-full px-2 py-1 border border-[#c2c6d3] rounded focus:outline-none focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] bg-white text-[#121c2a]"
                  />
                </Td>
                <Td className="text-right font-bold text-[#121c2a]">
                  ₹{calculateItemTotal(item.qty, item.price, item.tax).toFixed(2)}
                </Td>
                <Td>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-[#ba1a1a] hover:text-[#8a0000] transition-colors p-1"
                  >
                    <Trash2 size={16} />
                  </button>
                </Td>
              </tr>
            ))}
            <tr>
              <td colSpan={9} className="p-3">
                <button
                  onClick={addItem}
                  className="flex items-center gap-2 text-[#004287] hover:text-[#235eac] transition-colors font-medium"
                >
                  <Plus size={18} />
                  Add Item
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
