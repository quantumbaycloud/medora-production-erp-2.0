import { useMemo, useState } from "react";
import {
  FileText,
  CloudUpload,
  Plus,
  Minus,
  Trash2,
  Pill,
  CreditCard,
  Banknote,
  QrCode,
  CheckCircle,
  ArrowRight,
} from "lucide-react";
import api, { withPharmacy } from "../../services/api";
import { createInvoice } from "../../services/billingService";
import { quickProducts as suggestedProducts } from "../../data/billing/billingData";

const initialPrescriptionItems = [];

const PrescriptionBilling = () => {
  const [cartItems, setCartItems] = useState(initialPrescriptionItems);
  const [searchQuery, setSearchQuery] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");


  const updateQuantity = (id, delta) => {
    setCartItems((prevItems) =>
      prevItems
        .map((item) => {
          const newQuantity = Math.max(0, item.quantity + delta);
          return { ...item, quantity: newQuantity, total: newQuantity * item.price };
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

  const filteredProducts = suggestedProducts.filter((product) =>
    String(product.name || "").toLowerCase().includes(searchQuery.trim().toLowerCase())
  ).slice(0, 8);

  const addProduct = (product) => {
    const existing = cartItems.find((item) => item.medicine_id === product.id && item.batch_number === product.batch_number);
    if (existing) {
      updateQuantity(existing.id, 1);
      return;
    }
    const price = Number(product.price || 0);
    setCartItems((prev) => [...prev, {
      ...product,
      id: `${product.id}:${product.batch_number || "default"}`,
      medicine_id: product.id,
      batch: product.batch_number,
      batch_number: product.batch_number,
      quantity: 1,
      price,
      total: price,
      gst_percentage: Number(product.gst_percentage || 0),
    }]);
    setSearchQuery("");
  };

  const { subtotal, tax, total } = useMemo(() => {
    const rawSubtotal = cartItems.reduce((sum, item) => sum + Number(item.total || 0), 0);
    const computedTax = cartItems.reduce((sum, item) => sum + Number(item.total || 0) * Number(item.gst_percentage || 0) / 100, 0);
    const grandTotal = rawSubtotal + computedTax;
    return { subtotal: rawSubtotal, tax: computedTax, total: grandTotal };
  }, [cartItems]);

  const handleUpload = async (event) => {
    const file = event.target?.files?.[0];
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { setUploadMessage("Prescription file exceeds the configured 10MB limit."); return; }
    setUploading(true); setUploadMessage("");
    try {
      const form = new FormData();
      form.append("file", file);
      const { data } = await api.post("/prescriptions/upload", form, { params: withPharmacy(), headers: { "Content-Type": "multipart/form-data" } });
      setUploadMessage(data?.message || "Prescription uploaded successfully.");
    } catch (error) {
      setUploadMessage(error?.response?.data?.detail || "Prescription upload failed.");
    } finally { setUploading(false); }
  };

  const handleCheckout = async () => {
    if (!cartItems.length) { setUploadMessage("Add at least one medicine before checkout."); return; }
    setUploading(true); setUploadMessage("");
    try {
      await createInvoice({ cartItems, paymentMethod: paymentMethod === "cash" ? "Cash" : paymentMethod === "upi" ? "UPI" : "Card" });
      clearCart();
      setUploadMessage("Invoice created successfully.");
    } catch (error) {
      setUploadMessage(error?.response?.data?.detail || error?.message || "Unable to create invoice.");
    } finally { setUploading(false); }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files?.[0];
    if (file) handleUpload({ target: { files: [file] } });
  };

  return (
    <div className="flex h-[calc(100vh-80px)] flex-col gap-6 overflow-hidden">
      <header className="shrink-0">
        <h1 className="text-2xl font-bold tracking-tight text-on-background">
          Prescription Billing
        </h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Add items from uploaded prescriptions and process secure medical
          transactions.
        </p>
      </header>

      <div className="flex flex-1 gap-6 overflow-hidden">
        {/* LEFT PANEL: Prescription & Cart */}
        <div className="flex flex-1 flex-col gap-6 overflow-hidden">
          {/* Upload/Attach Prescription Section */}
          <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="flex items-center gap-2 text-lg font-semibold text-on-background">
                <FileText size={20} className="text-primary" />
                Prescription Attachment
              </h3>
              <span className="rounded bg-secondary-container px-2 py-1 text-xs font-bold text-teal-700">
                SECURE UPLOAD
              </span>
            </div>
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 transition-colors ${
                isDragging
                  ? "border-primary bg-primary-fixed"
                  : "border-outline bg-surface-container-low hover:border-primary hover:bg-surface-container"
              }`}
            >
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary-fixed transition-transform group-hover:scale-110">
                <CloudUpload size={36} className="text-primary" />
              </div>
              <p className="text-base font-semibold text-on-background">
                Drop prescription PDF or image here
              </p>
              <p className="mt-1 text-sm text-on-surface-variant">
                Maximum file size 10MB (JPG, PNG, PDF)
              </p>
              <label className="mt-6 cursor-pointer rounded-lg border border-primary px-6 py-2 text-sm text-primary transition-all hover:bg-primary hover:text-on-primary">
                {uploading ? "Uploading…" : "Browse Files"}
                <input type="file" accept="image/jpeg,image/png,application/pdf" className="hidden" onChange={handleUpload} disabled={uploading} />
              </label>
              {uploadMessage && <p className="mt-3 text-sm text-on-surface-variant">{uploadMessage}</p>}
            </div>
          </div>

          {/* Product Search & Cart Table */}
          <div className="flex flex-1 flex-col overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
            <div className="border-b border-outline-variant p-6">
              <div className="relative">
                <Pill
                  size={20}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-primary"
                />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(event) => setSearchQuery(event.target.value)}
                  placeholder="Search for prescribed medicine (e.g. Amoxicillin, Paracetamol)..."
                  className="w-full rounded-lg border border-outline-variant bg-surface-container-low py-3 pl-12 pr-4 text-base transition-all focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary-fixed"
                />
                {searchQuery.trim() && filteredProducts.length > 0 && (
                  <div className="absolute left-0 right-0 top-full z-20 mt-2 overflow-hidden rounded-lg border border-outline-variant bg-surface-container-lowest shadow-lg">
                    {filteredProducts.map((product) => (
                      <button key={`${product.id}-${product.batch_number || ""}`} type="button" onClick={() => addProduct(product)} className="flex w-full items-center justify-between border-b border-outline-variant px-4 py-3 text-left last:border-b-0 hover:bg-surface-container-low">
                        <span><span className="block text-sm font-semibold">{product.name}</span><span className="text-xs text-on-surface-variant">Batch {product.batch_number || "—"} · Stock {product.stock ?? 0}</span></span>
                        <span className="text-sm font-semibold">₹{Number(product.price || 0).toFixed(2)}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="flex-1 overflow-auto">
              <table className="w-full border-collapse text-left">
                <thead className="sticky top-0 z-10 bg-surface-container">
                  <tr>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Medicine Name
                    </th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Batch
                    </th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Price
                    </th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Qty
                    </th>
                    <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Total
                    </th>
                    <th className="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant">
                  {cartItems.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-16 text-center">
                        <Pill size={28} className="mx-auto mb-2 text-slate-300" />
                        <p className="text-sm italic text-on-surface-variant">
                          Search above to add more medicines from the
                          prescription...
                        </p>
                      </td>
                    </tr>
                  ) : (
                    cartItems.map((item) => (
                      <tr key={item.id} className="transition-colors hover:bg-surface-container-low">
                        <td className="px-6 py-4">
                          <div className="flex flex-col">
                            <span className="text-sm font-bold text-on-background">
                              {item.name}
                            </span>
                            <span className="text-xs italic text-on-surface-variant">
                              {item.category}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-on-surface-variant">
                          {item.batch}
                        </td>
                        <td className="px-6 py-4 text-sm text-on-background">
                          ₹{Number(item.price || 0).toFixed(2)}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex w-fit items-center overflow-hidden rounded-lg border border-outline-variant">
                            <button
                              type="button"
                              onClick={() => updateQuantity(item.id, -1)}
                              className="bg-surface-container px-2 py-1 text-on-surface-variant transition-colors hover:bg-surface-container-high"
                            >
                              <Minus size={14} />
                            </button>
                            <input
                              type="text"
                              value={item.quantity}
                              readOnly
                              className="w-10 border-none text-center text-sm focus:ring-0"
                            />
                            <button
                              type="button"
                              onClick={() => updateQuantity(item.id, 1)}
                              className="bg-surface-container px-2 py-1 text-on-surface-variant transition-colors hover:bg-surface-container-high"
                            >
                              <Plus size={14} />
                            </button>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm font-bold text-primary">
                          ₹{Number(item.total || 0).toFixed(2)}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button
                            type="button"
                            onClick={() => removeItem(item.id)}
                            className="rounded-lg p-2 text-error transition-colors hover:bg-error-container"
                            aria-label={`Remove ${item.name}`}
                          >
                            <Trash2 size={18} />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            {cartItems.length > 0 && (
              <div className="flex items-center justify-between border-t border-outline-variant p-6">
                <button
                  type="button"
                  onClick={clearCart}
                  className="flex items-center gap-2 text-sm font-semibold text-error transition hover:underline"
                >
                  <Trash2 size={16} />
                  Clear All
                </button>
                <p className="text-sm text-on-surface-variant">
                  {cartItems.length} item{cartItems.length !== 1 ? "s" : ""} in
                  cart
                </p>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT PANEL: Summary & Checkout */}
        <div className="flex w-[380px] shrink-0 flex-col gap-6 overflow-y-auto">
          {/* Order Summary */}
          <div className="relative overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
            <div className="absolute right-0 top-0 h-32 w-32 -translate-y-16 translate-x-16 rounded-full bg-linear-to-br from-primary to-secondary opacity-10" />
            <h3 className="relative z-10 mb-6 text-lg font-semibold text-on-background">
              Order Summary
            </h3>
            <div className="relative z-10 space-y-4">
              <div className="flex items-center justify-between text-sm text-on-surface-variant">
                <span>Subtotal</span>
                <span className="font-semibold text-on-background">₹{subtotal.toFixed(2)}</span>
              </div>
              <div className="flex items-center justify-between text-sm text-on-surface-variant">
                <span>GST</span>
                <span className="font-semibold text-on-background">₹{tax.toFixed(2)}</span>
              </div>
              <div className="flex items-center justify-between border-t border-dashed border-outline pt-4">
                <span className="text-base font-semibold text-on-background">Grand Total</span>
                <span className="text-xl font-bold text-primary">₹{total.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Payment Methods */}
          <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm">
            <h3 className="mb-4 text-xs font-bold uppercase tracking-widest text-on-surface-variant">
              Payment Method
            </h3>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: "cash", label: "Cash", icon: Banknote },
                { id: "card", label: "Card", icon: CreditCard },
                { id: "upi", label: "UPI", icon: QrCode },
              ].map((method) => {
                const Icon = method.icon;
                const isSelected = paymentMethod === method.id;
                return (
                  <button
                    key={method.id}
                    type="button"
                    onClick={() => setPaymentMethod(method.id)}
                    className={`flex flex-col items-center gap-2 rounded-xl p-4 transition-all ${
                      isSelected
                        ? "border-2 border-primary bg-primary-fixed text-primary"
                        : "border-2 border-outline-variant hover:border-primary/50"
                    }`}
                  >
                    <Icon size={22} />
                    <span className="text-[10px] font-bold uppercase">
                      {method.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Create Invoice */}
          <button
            type="button"
            disabled={uploading || !cartItems.length}
            onClick={handleCheckout}
            className="flex w-full items-center justify-center gap-3 rounded-xl bg-primary py-5 text-base font-bold text-on-primary shadow-lg transition-all hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <CheckCircle size={22} />
            <span>{uploading ? "Processing…" : "Create Invoice"}</span>
            <span className="text-lg font-extrabold">₹{total.toFixed(2)}</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </div>
      </div>
  );
};

export default PrescriptionBilling;