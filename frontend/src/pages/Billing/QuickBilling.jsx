import { useMemo, useState } from "react";
import {
  Search,
  Plus,
  Minus,
  Trash2,
  ShoppingCart,
  ChevronRight,
  Tag,
  CreditCard,
  Banknote,
  CheckCircle,
  Pause,
  Play,
} from "lucide-react";

import { useCart } from "../../hooks/useCart";
import { quickProducts } from "../../data/billing/billingData";
import { createInvoice } from "../../services/billingService";

const TAX_RATE = 0.085;

const categories = ["All Items"];

const QuickBilling = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("All Items");
  const [showReceipt, setShowReceipt] = useState(false);
  const {
    cartItems,
    setCartItems,
    isHeld,
    holdBill,
    resumeBill,
    paymentMethod,
    setPaymentMethod,
    updateQuantity,
    removeItem,
    clearCart,
    subtotal,
    tax,
    total,
  } = useCart([], TAX_RATE);

  const filteredProducts = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();
    return quickProducts.filter((product) => {
      const matchesCategory =
        activeCategory === "All Items" || product.category === activeCategory;
      const matchesSearch =
        !normalizedQuery || product.name.toLowerCase().includes(normalizedQuery);
      return matchesCategory && matchesSearch;
    });
  }, [searchQuery, activeCategory]);

  const addToCart = (product) => {
    setCartItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.id === product.id);
      if (existingItem) {
        return prevItems.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [
        ...prevItems,
        {
          id: product.id,
          name: product.name,
          description: product.category,
          price: product.price,
          batch_number: product.batch_number,
          quantity: 1,
        },
      ];
    });
  };

  const handleCharge = () => {
    if (cartItems.length === 0) {
      alert("Cart is empty. Click on items to add them.");
      return;
    }
    if (isHeld) {
      alert("Bill is on hold. Resume before charging.");
      return;
    }
    setShowReceipt(true);
  };

  const handleConfirmCharge = async () => {
    try {
      await createInvoice({ cartItems, paymentMethod: paymentMethod === "card" ? "Card" : "Cash" });
      setShowReceipt(false);
      clearCart();
    } catch (error) { alert(error?.response?.data?.detail || error.message || "Unable to create invoice"); }
  };

  return (
    <div className="flex h-[calc(100vh-80px)] gap-6 overflow-hidden">
      {/* LEFT PANEL: Products & Categories */}
      <section className="flex min-w-0 flex-1 flex-col overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest">
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-outline-variant bg-surface-container-low p-4">
          <div className="no-scrollbar flex flex-1 space-x-2 overflow-x-auto pb-1">
            {categories.map((category) => (
              <button
                key={category}
                type="button"
                onClick={() => setActiveCategory(category)}
                className={`whitespace-nowrap rounded-full px-4 py-1.5 text-xs font-bold transition ${
                  activeCategory === category
                    ? "border border-primary bg-primary-fixed text-primary"
                    : "border border-outline-variant bg-surface-container-lowest text-on-surface-variant hover:bg-surface-container"
                }`}
              >
                {category}
              </button>
            ))}
          </div>
          <div className="relative ml-4 w-64 shrink-0">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-outline"
            />
            <input
              type="text"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder="Scan or type barcode..."
              className="w-full rounded border border-outline-variant bg-surface-container py-1.5 pl-10 pr-4 text-sm transition-colors focus:border-primary focus:outline-none focus:ring-0"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto bg-surface-container-lowest p-4">
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
            {filteredProducts.length === 0 ? (
              <div className="col-span-full flex flex-col items-center gap-3 py-16 text-center">
                <Search size={28} className="text-slate-300" />
                <p className="text-sm text-on-surface-variant">
                  No products found. Try a different search or category.
                </p>
              </div>
            ) : (
              filteredProducts.map((product) => (
                <button
                  key={product.id}
                  type="button"
                  onClick={() => addToCart(product)}
                  className="group relative flex h-full cursor-pointer flex-col rounded border border-outline-variant bg-surface-container-low p-3 transition-all hover:border-primary hover:shadow-[0_4px_12px_rgba(0,81,213,0.1)]"
                >
                  {product.category === "Medicine" && (
                    <span className="absolute right-2 top-2 rounded bg-secondary-container px-2 py-0.5 text-[11px] font-medium text-teal-700">
                      Rx
                    </span>
                  )}
                  <div className="mb-3 flex h-24 w-full items-center justify-center overflow-hidden rounded bg-surface-container">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                  </div>
                  <div className="mt-auto">
                    <h3 className="mb-1 truncate text-sm font-medium leading-tight text-on-background">
                      {product.name}
                    </h3>
                    <p className="mb-2 text-xs text-on-surface-variant">{product.category}</p>
                    <div className="mt-2 flex items-center justify-between">
                      <span className="text-base font-semibold text-primary">
                        ${product.price.toFixed(2)}
                      </span>
                      <Plus
                        size={18}
                        className="text-slate-300 transition-colors group-hover:text-primary"
                      />
                    </div>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>
      </section>

      {/* RIGHT PANEL: Cart & Summary */}
      <section className="flex w-[380px] shrink-0 flex-col overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest">
        <div className="flex items-center justify-between border-b border-outline-variant bg-surface-container-low p-4">
          <div className="flex items-center">
            <ShoppingCart size={18} className="mr-2 text-primary" />
            <h2 className="text-base font-semibold text-primary">Current Bill</h2>
          </div>
          {cartItems.length > 0 && (
            <button
              type="button"
              onClick={clearCart}
              className="flex items-center border-none bg-transparent p-0 text-xs font-bold text-error hover:underline"
            >
              <Trash2 size={14} className="mr-1" />
              Clear
            </button>
          )}
        </div>

        <div className="group flex cursor-pointer items-center justify-between border-b border-outline-variant bg-surface-container-lowest px-4 py-3 transition-colors hover:bg-surface-container-low">
          <div className="flex items-center">
            <div className="mr-3 flex h-8 w-8 items-center justify-center rounded-full bg-primary-fixed text-xs font-bold text-blue-800">
              JD
            </div>
            <div>
              <p className="m-0 text-sm font-medium leading-tight text-on-background">Walk-in customer</p>
              <p className="m-0 text-xs text-on-surface-variant">Select a customer for this bill</p>
            </div>
          </div>
          <ChevronRight size={18} className="text-slate-300 transition-colors group-hover:text-primary" />
        </div>

        {isHeld && (
          <div className="flex items-center justify-between border-b border-tertiary-fixed-dim bg-tertiary-fixed px-4 py-3">
            <div className="flex items-center gap-2">
              <Pause size={16} className="text-tertiary" />
              <span className="text-sm font-semibold text-on-tertiary-fixed-variant">Bill is on hold</span>
            </div>
            <button
              type="button"
              onClick={resumeBill}
              className="flex items-center gap-1 rounded bg-tertiary px-3 py-1 text-xs font-bold text-on-primary transition hover:bg-tertiary-container"
            >
              <Play size={14} />
              Resume
            </button>
          </div>
        )}

        <div className="flex-1 overflow-y-auto bg-surface-container-lowest">
          <ul className="divide-y divide-outline-variant border-b border-outline-variant">
            {cartItems.length === 0 ? (
              <li className="flex flex-col items-center gap-3 px-4 py-16 text-center">
                <ShoppingCart size={28} className="text-slate-300" />
                <p className="text-sm italic text-on-surface-variant">
                  Your cart is empty. Click on items to add them.
                </p>
              </li>
            ) : (
              cartItems.map((item) => (
                <li key={item.id} className="group flex items-start p-4 transition-colors hover:bg-surface-container-low">
                  <div className="min-w-0 flex-1 pr-4">
                    <div className="mb-1 flex items-start justify-between">
                      <h4 className="m-0 truncate text-sm font-medium text-on-background">
                        {item.name}
                      </h4>
                      <span className="ml-2 text-sm font-medium text-primary">
                        ${(item.quantity * item.price).toFixed(2)}
                      </span>
                    </div>
                    <p className="m-0 mb-2 text-xs text-on-surface-variant">{item.description}</p>
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center overflow-hidden rounded border border-outline-variant bg-surface-container">
                        <button
                          type="button"
                          onClick={() => updateQuantity(item.id, -1)}
                          className="px-2 py-1 text-on-surface-variant transition-colors hover:bg-surface-container-high"
                        >
                          <Minus size={14} />
                        </button>
                        <input
                          type="text"
                          value={item.quantity}
                          readOnly
                          className="w-8 border-none bg-transparent p-0 text-center text-sm focus:ring-0"
                        />
                        <button
                          type="button"
                          onClick={() => updateQuantity(item.id, 1)}
                          className="px-2 py-1 text-on-surface-variant transition-colors hover:bg-surface-container-high"
                        >
                          <Plus size={14} />
                        </button>
                      </div>
                      <button
                        type="button"
                        onClick={() => removeItem(item.id)}
                        className="text-slate-300 opacity-0 transition-all hover:text-error group-hover:opacity-100"
                        aria-label={`Remove ${item.name}`}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </li>
              ))
            )}
          </ul>

          <div className="p-4">
            <button
              type="button"
              onClick={() => alert("Coupon code input opened.")}
              className="flex w-full items-center justify-center rounded border border-dashed border-outline py-2 text-sm text-on-surface-variant transition-colors hover:border-primary hover:text-primary"
            >
              <Tag size={16} className="mr-2" />
              Add Discount Code
            </button>
          </div>
        </div>

        <div className="shrink-0 border-t border-outline-variant bg-surface-container-low p-4">
          <div className="mb-4 space-y-2">
            <div className="flex justify-between text-sm text-on-surface-variant">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm text-on-surface-variant">
              <span>Tax (8.5%)</span>
              <span>${tax.toFixed(2)}</span>
            </div>
            <div className="mt-2 flex justify-between border-t border-dashed border-outline pt-2 text-base font-bold text-primary">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
          </div>

          <div className="mb-3 grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={isHeld ? resumeBill : holdBill}
              className={`flex items-center justify-center rounded border px-2 py-2 text-xs font-bold transition-colors ${
                isHeld
                  ? "border-amber-300 bg-tertiary-fixed text-on-tertiary-fixed-variant"
                  : "border-slate-400 text-on-background hover:bg-surface-container"
              }`}
            >
              {isHeld ? <Play size={14} className="mr-1" /> : <Pause size={14} className="mr-1" />}
              {isHeld ? "Resume" : "Hold"}
            </button>
            <button
              type="button"
              onClick={() => setPaymentMethod("card")}
              className={`flex items-center justify-center rounded border px-2 py-2 text-xs font-bold transition-colors ${
                paymentMethod === "card"
                  ? "border-primary bg-primary-fixed text-primary"
                  : "border-slate-400 text-on-background hover:bg-surface-container"
              }`}
            >
              <CreditCard size={14} className="mr-1" />
              Card
            </button>
            <button
              type="button"
              onClick={() => setPaymentMethod("cash")}
              className={`flex items-center justify-center rounded border px-2 py-2 text-xs font-bold transition-colors ${
                paymentMethod === "cash"
                  ? "border-primary bg-primary-fixed text-primary"
                  : "border-slate-400 text-on-background hover:bg-surface-container"
              }`}
            >
              <Banknote size={14} className="mr-1" />
              Cash
            </button>
          </div>

          <button
            type="button"
            onClick={handleCharge}
            className="flex w-full items-center justify-between rounded bg-linear-to-br from-primary to-secondary px-4 py-3 text-xs font-bold text-on-primary shadow-sm transition-all hover:from-primary-700 hover:to-secondary-600"
          >
            <span>Charge</span>
            <span className="text-lg font-bold leading-none">${total.toFixed(2)}</span>
          </button>
        </div>
      </section>

      {/* Payment Confirmation Modal */}
      {showReceipt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-inverse-surface/50 p-4">
          <div className="w-full max-w-md rounded-xl bg-surface-container-lowest p-6 shadow-2xl">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-lg font-bold text-on-background">Confirm Charge</h3>
              <button
                type="button"
                onClick={() => setShowReceipt(false)}
                className="rounded-full p-1 text-outline transition hover:bg-surface-container hover:text-on-surface-variant"
                aria-label="Close"
              >
                <Trash2 size={18} />
              </button>
            </div>

            <div className="mb-4 space-y-2 rounded-lg bg-surface-container-low p-4 text-sm">
              <div className="flex justify-between text-on-surface-variant">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-on-surface-variant">
                <span>Tax (8.5%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between border-t border-outline-variant pt-2 text-base font-bold text-on-background">
                <span>Total</span>
                <span>${total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-on-surface-variant">
                <span>Payment Method</span>
                <span className="font-semibold uppercase">{paymentMethod}</span>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => setShowReceipt(false)}
                className="flex-1 rounded-lg border border-outline-variant py-3 text-sm font-bold text-on-surface-variant transition hover:bg-surface-container-low"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleConfirmCharge}
                className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-linear-to-br from-primary to-secondary py-3 text-sm font-bold text-on-primary shadow-md transition hover:brightness-110"
              >
                <CheckCircle size={18} />
                Confirm Charge
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuickBilling;