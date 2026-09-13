import { useState, useCallback, useMemo } from "react";
import { Send } from "lucide-react";
import { Toast } from "../../components/purchases/Shared";
import OrderDetailsSection from "../../components/purchases/OrderDetailsSection";
import LineItemsTable from "../../components/purchases/LineItemsTable";
import NotesAndSummary from "../../components/purchases/NotesAndSummary";
import { initialOrderItems, productOptions, supplierOptions, locationOptions } from "../../data/purchases/data";
import erpApi from "../../services/erpApi";

export default function PurchaseOrderPage() {
  const [poNumber] = useState(() => `PO-${new Date().getFullYear()}-${Date.now().toString().slice(-6)}`);
  const [supplier, setSupplier] = useState("");
  const [location, setLocation] = useState("");
  const [poDate, setPoDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [deliveryDate, setDeliveryDate] = useState("");
  const [refNumber, setRefNumber] = useState("");
  const [items, setItems] = useState(initialOrderItems);
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState(null);

  const calculateItemTotal = useCallback((qty, price, tax) => {
    const subtotal = qty * price;
    return subtotal + subtotal * tax;
  }, []);

  const totals = useMemo(() => {
    let subtotal = 0;
    let taxTotal = 0;
    items.forEach((item) => {
      const itemSubtotal = item.qty * item.price;
      const itemTax = itemSubtotal * item.tax;
      subtotal += itemSubtotal;
      taxTotal += itemTax;
    });
    return { subtotal, taxTotal, grandTotal: subtotal + taxTotal };
  }, [items]);

  const updateItem = useCallback((id, field, value) => {
    setItems((prev) =>
      prev.map((item) => {
        if (item.id !== id) return item;
        const updated = { ...item, [field]: value };
        if (field === "product") {
          const product = productOptions.find((p) => p.id === value);
          if (product) {
            updated.sku = product.sku;
            updated.price = product.price;
          }
        }
        return updated;
      })
    );
  }, []);

  const addItem = useCallback(() => {
    const newId = `item-${Date.now()}`;
    setItems((prev) => [
      ...prev,
      { id: newId, product: "", sku: "", qty: 1, unit: "units", price: 0, tax: 0 },
    ]);
  }, []);

  const removeItem = useCallback((id) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const showToast = (message) => {
    setToast({ type: "success", message });
    setTimeout(() => setToast(null), 3000);
  };

  const buildPurchasePayload = () => {
    const validItems = items.filter((item) => item.product);
    if (!supplier) throw new Error("Please select a supplier");
    if (!validItems.length) throw new Error("Add at least one medicine to the order");
    return {
      supplier_id: supplier,
      branch_id: location || null,
      invoice_number: poNumber,
      invoice_date: poDate,
      paid_amount: 0,
      notes: [refNumber && `Reference: ${refNumber}`, notes].filter(Boolean).join("\n") || null,
      items: validItems.map((item) => ({
        medicine_id: item.product,
        batch_number: `PO-${poNumber}`,
        expiry_date: new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().slice(0, 10),
        quantity: Number(item.qty),
        free_quantity: 0,
        purchase_price: Number(item.price || 0),
        mrp: Number(item.price || 0),
        selling_price: Number(item.price || 0),
        tax_percentage: Number(item.tax || 0),
        discount_percentage: 0,
      })),
    };
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await erpApi.createPurchase(buildPurchasePayload());
      showToast("Purchase invoice draft saved in the ERP database.");
    } catch (error) {
      showToast(error?.response?.data?.detail || error.message || "Unable to save purchase.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSaveDraft = async () => {
    setIsSubmitting(true);
    try {
      await erpApi.createPurchase(buildPurchasePayload());
      showToast("Purchase draft saved successfully.");
    } catch (error) {
      showToast(error?.response?.data?.detail || error.message || "Unable to save draft.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#f8f9ff]">
      {toast && <Toast type={toast.type} message={toast.message} onClose={() => setToast(null)} />}

      <main className="flex-1 overflow-y-auto p-6 pb-32">
        <div className="max-w-7xl mx-auto space-y-6">
          <h2 className="font-headline-lg-mobile md:hidden text-[#121c2a] mb-4 font-bold tracking-tight">
            Create Purchase Order
          </h2>

          <OrderDetailsSection
            poNumber={poNumber}
            supplier={supplier}
            setSupplier={setSupplier}
            location={location}
            setLocation={setLocation}
            poDate={poDate}
            setPoDate={setPoDate}
            deliveryDate={deliveryDate}
            setDeliveryDate={setDeliveryDate}
            refNumber={refNumber}
            setRefNumber={setRefNumber}
            supplierOptions={supplierOptions}
          />

          <LineItemsTable
            items={items}
            updateItem={updateItem}
            addItem={addItem}
            removeItem={removeItem}
            calculateItemTotal={calculateItemTotal}
          />

          <NotesAndSummary notes={notes} setNotes={setNotes} totals={totals} />
        </div>
      </main>

      <div className="bg-white border-t border-[#c2c6d3] p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-20 flex justify-between items-center fixed bottom-0 left-0 md:left-64 right-0">
        <button className="px-6 py-2 text-[#424751] font-label-md hover:bg-[#eff4ff] border border-transparent hover:border-[#c2c6d3] rounded transition-all">
          Cancel
        </button>
        <div className="flex gap-3">
          <button
            onClick={handleSaveDraft}
            className="px-6 py-2 border rounded font-label-md transition-colors hover:bg-[#eff4ff] hidden sm:block border-[#004287] text-[#004287]"
          >
            Save as Draft
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="px-8 py-2 rounded font-label-md shadow-sm flex items-center gap-2 text-white bg-[#004287] hover:bg-[#235eac] transition-colors disabled:opacity-70"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Submitting...
              </>
            ) : (
              <>
                <Send size={18} />
                Submit Order
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
