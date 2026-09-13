import { useMemo, useState } from "react";
import {
  Search,
  Plus,
  Minus,
  Trash2,
  CheckCircle,
  CreditCard,
  Banknote,
} from "lucide-react";
import { suggestedProducts } from "../../data/billing/billingData";
import { createInvoice } from "../../services/billingService";

const TAX_RATE = 0.08;

const initialCartItems = [];

const ManualBilling = () => {
  const [cartItems, setCartItems] = useState(initialCartItems);
  const [searchQuery, setSearchQuery] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("card");

  const updateQuantity = (id, delta) => {
    setCartItems((prevItems) =>
      prevItems
        .map((item) => {
          const newQuantity = Math.max(0, item.quantity + delta);
          return { ...item, quantity: newQuantity };
        })
        .filter((item) => item.quantity > 0)
    );
  };

  const removeItem = (id) => {
    setCartItems((prevItems) => prevItems.filter((item) => item.id !== id));
  };

  const clearCart = () => {
    setCartItems([]);
  };

  const { subtotal, tax, total } = useMemo(() => {
    const rawSubtotal = cartItems.reduce(
      (sum, item) => sum + item.quantity * item.price,
      0
    );
    const computedTax = rawSubtotal * TAX_RATE;
    return {
      subtotal: rawSubtotal,
      tax: computedTax,
      total: rawSubtotal + computedTax,
    };
  }, [cartItems]);

  const handleAddItem = () => {
    if (!searchQuery.trim()) return;
    const trimmed = searchQuery.trim();
    setCartItems((prevItems) => [
      ...prevItems,
      {
        id: Date.now(),
        name: trimmed,
        sku: "N/A",
        price: 0,
        quantity: 1,
      },
    ]);
    setSearchQuery("");
  };

  const handleCompleteSale = async () => {
    try { await createInvoice({ cartItems, paymentMethod: paymentMethod === "card" ? "Card" : "Cash" }); clearCart(); } catch (error) { alert(error?.response?.data?.detail || error.message || "Unable to create invoice"); }
  };

  return (
    <div className="flex h-[calc(100vh-80px)] gap-6 overflow-hidden">
      {/* LEFT PANEL: Cart & Search */}
      <div className="flex flex-1 flex-col gap-6 overflow-hidden">
        <div className="flex h-full flex-col gap-6 rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
          {/* Search & Add */}
          <div className="flex items-end gap-4">
            <div className="flex flex-1 flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                Search Product / SKU
              </label>
              <div className="relative">
                <Search
                  size={18}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-outline"
                />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(event) => setSearchQuery(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") handleAddItem();
                  }}
                  placeholder="Scan barcode or type name..."
                  className="w-full rounded border border-outline-variant bg-surface-container-lowest py-3 pl-10 pr-4 text-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>
            <button
              type="button"
              onClick={handleAddItem}
              className="flex h-[48px] items-center gap-2 rounded bg-linear-to-br from-primary to-secondary px-6 py-3 text-xs font-bold text-on-primary"
            >
              <Plus size={16} />
              Add Item
            </button>
          </div>

          {/* Cart Table */}
          <div className="flex flex-1 flex-col overflow-hidden rounded-lg border border-outline-variant bg-surface-container-lowest">
            {/* Header Row */}
            <div className="grid grid-cols-12 gap-4 border-b border-outline-variant bg-surface-container-low p-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
              <div className="col-span-5">Product</div>
              <div className="col-span-2 text-center">Qty</div>
              <div className="col-span-2 text-right">Price</div>
              <div className="col-span-2 text-right">Total</div>
              <div className="col-span-1 text-center"></div>
            </div>

            <div className="flex-1 overflow-y-auto">
              {cartItems.length === 0 ? (
                <div className="flex flex-col items-center gap-3 py-16 text-center">
                  <Search size={28} className="text-slate-300" />
                  <p className="text-sm italic text-on-surface-variant">
                    Cart is empty. Search above to add items.
                  </p>
                </div>
              ) : (
                cartItems.map((item) => {
                  const itemTotal = item.quantity * item.price;
                  return (
                    <div
                      key={item.id}
                      className="grid grid-cols-12 items-center gap-4 border-b border-outline-variant p-4 transition-colors hover:bg-surface-container-low"
                    >
                      <div className="col-span-5 flex flex-col">
                        <span className="text-sm font-semibold text-on-background">
                          {item.name}
                        </span>
                        <span className="text-xs text-on-surface-variant">
                          SKU: {item.sku}
                        </span>
                      </div>
                      <div className="col-span-2 flex items-center justify-center gap-2">
                        <button
                          type="button"
                          onClick={() => updateQuantity(item.id, -1)}
                          className="flex h-8 w-8 items-center justify-center rounded border border-outline-variant text-primary transition-colors hover:border-primary"
                        >
                          <Minus size={14} />
                        </button>
                        <span className="w-6 text-center text-sm font-semibold">
                          {item.quantity}
                        </span>
                        <button
                          type="button"
                          onClick={() => updateQuantity(item.id, 1)}
                          className="flex h-8 w-8 items-center justify-center rounded border border-outline-variant text-primary transition-colors hover:border-primary"
                        >
                          <Plus size={14} />
                        </button>
                      </div>
                      <div className="col-span-2 text-right text-sm text-on-surface-variant">
                        ${item.price.toFixed(2)}
                      </div>
                      <div className="col-span-2 text-right text-sm font-semibold text-on-background">
                        ${itemTotal.toFixed(2)}
                      </div>
                      <div className="col-span-1 text-center">
                        <button
                          type="button"
                          onClick={() => removeItem(item.id)}
                          className="text-error transition-colors hover:text-rose-300"
                          aria-label={`Remove ${item.name}`}
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>
                  );
                })
              )}
            </div>

            {cartItems.length > 0 && (
              <div className="flex items-center justify-between border-t border-outline-variant p-4">
                <button
                  type="button"
                  onClick={clearCart}
                  className="flex items-center gap-1 text-xs font-bold text-error transition hover:underline"
                >
                  <Trash2 size={14} />
                  Clear All
                </button>
                <p className="text-xs text-on-surface-variant">
                  {cartItems.length} item{cartItems.length !== 1 ? "s" : ""} in
                  cart
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* RIGHT PANEL: Summary & Payment */}
      <div className="flex w-[380px] flex-col gap-6 overflow-y-auto">
        <div className="flex flex-col gap-6 rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
          <h2 className="border-b border-outline-variant pb-4 text-lg font-semibold text-on-background">
            Bill Summary
          </h2>

          <div className="flex flex-col gap-3 text-sm">
            <div className="flex items-center justify-between text-on-surface-variant">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between text-on-surface-variant">
              <span>Tax (8%)</span>
              <span>${tax.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between text-on-surface-variant">
              <span>Discount</span>
              <span className="text-teal-700">-$0.00</span>
            </div>
            <div className="mt-2 flex items-center justify-between border-t border-outline-variant pt-3">
              <span className="text-base font-semibold text-on-background">Total</span>
              <span className="text-base font-semibold text-primary">
                ${total.toFixed(2)}
              </span>
            </div>
          </div>

          <div className="mt-4 flex flex-col gap-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
              Payment Method
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setPaymentMethod("card")}
                className={`flex flex-col items-center gap-2 rounded-lg p-3 transition-colors ${
                  paymentMethod === "card"
                    ? "border-2 border-primary bg-primary-fixed text-on-background"
                    : "border border-outline-variant bg-surface-container-lowest text-on-surface-variant hover:border-primary hover:text-primary"
                }`}
              >
                <CreditCard size={20} className={paymentMethod === "card" ? "text-primary" : ""} />
                <span className="text-xs font-bold">Card</span>
              </button>
              <button
                type="button"
                onClick={() => setPaymentMethod("cash")}
                className={`flex flex-col items-center gap-2 rounded-lg p-3 transition-colors ${
                  paymentMethod === "cash"
                    ? "border-2 border-primary bg-primary-fixed text-on-background"
                    : "border border-outline-variant bg-surface-container-lowest text-on-surface-variant hover:border-primary hover:text-primary"
                }`}
              >
                <Banknote size={20} className={paymentMethod === "cash" ? "text-primary" : ""} />
                <span className="text-xs font-bold">Cash</span>
              </button>
            </div>
          </div>

          <div className="mt-4 flex flex-col gap-3">
            <button
              type="button"
              onClick={handleCompleteSale}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-linear-to-br from-primary to-secondary py-4 text-sm font-bold text-on-primary shadow-sm"
            >
              <CheckCircle size={20} />
              Complete Sale
            </button>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                className="rounded-lg border border-outline-variant py-3 text-xs font-bold text-on-surface-variant transition-colors hover:bg-surface-container-low"
              >
                Hold Bill
              </button>
              <button
                type="button"
                className="rounded-lg border border-outline-variant py-3 text-xs font-bold text-error transition-colors hover:bg-error-container"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ManualBilling;