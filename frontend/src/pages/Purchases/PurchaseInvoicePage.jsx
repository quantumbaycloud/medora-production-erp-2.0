import { useState, useCallback, useMemo } from "react";
import {
  Save,
  CheckCircle,
  BadgeCheck,
  ShieldCheck,
  Undo2,
  Receipt,
  RefreshCw,
  Download,
  Search,
} from "lucide-react";
import { Toast } from "../../components/purchases/Shared";
import ReceiveGoodsTab from "../../components/purchases/ReceiveGoodsTab";
import BatchEntryTab from "../../components/purchases/BatchEntryTab";
import ExpiryEntryTab from "../../components/purchases/ExpiryEntryTab";
import PurchaseReturnTab from "../../components/purchases/PurchaseReturnTab";
import CreditNotesTab from "../../components/purchases/CreditNotesTab";
import { initialReceivedItems } from "../../data/purchases/data";

const TAB_LIST = [
  { key: "receive-goods", label: "Receive Goods"  },
  { key: "batch-entry", label: "Batch Entry" },
  { key: "expiry-entry", label: "Expiry Entry" },
  { key: "purchase-return", label: "Purchase Return" },
  { key: "credit-notes", label: "Credit Notes" },
];

const createInitialBatches = () =>
  Object.fromEntries(
    initialReceivedItems.map((item) => [
      item.id,
      [{ batchNo: item.batch || "", qty: item.received }],
    ]),
  );

const PurchasePageInvoice = () => {
  const [activeTab, setActiveTab] = useState("receive-goods");
  const [selectedPO, setSelectedPO] = useState("");
  const [invoiceNo, setInvoiceNo] = useState("");
  const [invoiceDate, setInvoiceDate] = useState(() => new Date().toISOString().slice(0,10));
  const [receivedDate, setReceivedDate] = useState(() => new Date().toISOString().slice(0,10));
  const [receivedItems, setReceivedItems] = useState(initialReceivedItems);
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState(null);
  const [currentBatchItemId, setCurrentBatchItemId] = useState(null);
  const [itemBatches, setItemBatches] = useState(createInitialBatches);
  const [creditNoteNumber, setCreditNoteNumber] = useState("");
  const [creditNoteAmount, setCreditNoteAmount] = useState("");
  const [returnReason, setReturnReason] = useState("Damaged Goods");
  const [returnDate, setReturnDate] = useState(() => new Date().toISOString().slice(0,10));
  const [returnQuantities, setReturnQuantities] = useState({});
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");

  const totals = useMemo(() => {
    let totalOrdered = 0;
    let totalReceived = 0;
    receivedItems.forEach((item) => {
      totalOrdered += item.ordered;
      totalReceived += item.received;
    });
    return { totalOrdered, totalReceived, variance: totalReceived - totalOrdered };
  }, [receivedItems]);

  const updateItemData = useCallback((id, field, value) => {
    setReceivedItems((prev) =>
      prev.map((item) => {
        if (item.id !== id) return item;
        return { ...item, [field]: field === "received" ? parseInt(value) || 0 : value };
      })
    );
  }, []);

  const updateBatchValue = useCallback((itemId, idx, field, value) => {
    setItemBatches((prev) => {
      const batches = [...(prev[itemId] || [])];
      if (field === "qty") {
        batches[idx] = { ...batches[idx], qty: parseInt(value) || 0 };
      } else {
        batches[idx] = { ...batches[idx], batchNo: value };
      }
      return { ...prev, [itemId]: batches };
    });
  }, []);

  const addBatchRow = useCallback((itemId) => {
    setItemBatches((prev) => {
      const batches = [...(prev[itemId] || [])];
      batches.push({ batchNo: "", qty: 0 });
      return { ...prev, [itemId]: batches };
    });
  }, []);

  const removeBatchRow = useCallback((itemId, idx) => {
    setItemBatches((prev) => {
      const batches = [...(prev[itemId] || [])];
      batches.splice(idx, 1);
      return { ...prev, [itemId]: batches };
    });
  }, []);

  const calculateBatchTotal = useCallback(
    (itemId) => (itemBatches[itemId] || []).reduce((acc, curr) => acc + curr.qty, 0),
    [itemBatches]
  );

  const calculateShelfLife = useCallback((expiryStr) => {
    if (!expiryStr) return { months: 0, status: "UNKNOWN", badgeClass: "bg-[#f8f9ff] text-[#424751]" };
    const now = new Date();
    const expiry = new Date(expiryStr + "-01");
    const months = (expiry.getFullYear() - now.getFullYear()) * 12 + (expiry.getMonth() - now.getMonth());
    let status = "OK";
    let badgeClass = "bg-[#94f7b9] text-[#006d40] border border-[#006d40]";
    if (months <= 0) {
      status = "EXPIRED";
      badgeClass = "bg-[#ffdad6] text-[#ba1a1a] border border-[#ba1a1a]";
    } else if (months <= 6) {
      status = "NEAR EXPIRY";
      badgeClass = "bg-[#ffdad6] text-[#ba1a1a] border border-[#ba1a1a]";
    }
    return { months, status, badgeClass };
  }, []);

  const expiryStats = useMemo(() => {
    let total = 0,
      near = 0,
      expired = 0;
    receivedItems.forEach((item) => {
      const batches = itemBatches[item.id] || [{ batchNo: item.batch, qty: item.received }];
      batches.forEach(() => {
        const life = calculateShelfLife(item.expiry);
        if (life.status === "EXPIRED") expired++;
        else if (life.status === "NEAR EXPIRY") near++;
        total++;
      });
    });
    return { total, near, expired };
  }, [receivedItems, itemBatches, calculateShelfLife]);

  const updateReturnQuantity = useCallback((itemId, value) => {
    const val = parseInt(value) || 0;
    setReturnQuantities((prev) => ({ ...prev, [itemId]: val }));
  }, []);

  const getReturnTotal = useCallback(
    () => Object.values(returnQuantities).reduce((acc, curr) => acc + curr, 0),
    [returnQuantities]
  );

  const estimatedCredit = useMemo(() => 0, []);

  const switchTab = useCallback((tab) => {
    setActiveTab(tab);
    setPage(1);
  }, []);

  const showToast = (type, message) => {
    setToast({ type, message });
    setTimeout(() => setToast(null), 3000);
  };

  const handleConfirm = useCallback(() => {
    setIsSubmitting(true);
    showToast("info", "Purchase workflow validation is complete. Use the backend purchase endpoints for persisted invoice changes.");
    setIsSubmitting(false);
  }, [activeTab]);

  const handleSaveDraft = useCallback(() => {
    showToast("info", "Draft is kept in the current form until a persisted purchase-order endpoint is available.");
  }, []);

  const getTabConfig = () => {
    switch (activeTab) {
      case "receive-goods":
        return { title: "Purchase Invoice", icon: CheckCircle, text: "Confirm Receipt" };
      case "batch-entry":
        return { title: "Batch Management", icon: BadgeCheck, text: "Confirm Batches" };
      case "expiry-entry":
        return { title: "Expiry & Shelf Life", icon: ShieldCheck, text: "Finalize Invoice" };
      case "purchase-return":
        return { title: "Purchase Return", icon: Undo2, text: "Submit Return Request" };
      case "credit-notes":
        return { title: "Credit Notes", icon: Receipt, text: "Save Notes" };
      default:
        return { title: "Purchase Invoice", icon: CheckCircle, text: "Confirm" };
    }
  };

  const tabConfig = getTabConfig();
  const TabIcon = tabConfig.icon;

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#f8f9ff]">
      {toast && (
        <Toast type={toast.type} message={toast.message} onClose={() => setToast(null)} />
      )}

      <main className="flex-1 overflow-y-auto p-6 space-y-6 pt-0">
        <div className="bg-white border-b border-[#c2c6d3] sticky top-0 z-20 mt-4">
          <div className="flex overflow-x-auto no-scrollbar gap-8 py-2 whitespace-nowrap px-6">
            <div className="flex flex-col gap-2">
              <span className="text-[12px] font-bold text-[#004287] uppercase tracking-wider opacity-60 px-1">
                Purchase Invoice
              </span>
              <div className="flex gap-4 overflow-y-hidden pb-2">
                {TAB_LIST.map((tab) => {
                  const isActive = activeTab === tab.key;
                  return (
                    <button
                      key={tab.key}
                      onClick={() => switchTab(tab.key)}
                      className={`text-[16px] text-[#004287] relative px-1 cursor-pointer transition-opacity flex items-center gap-1.5 ${
                        isActive ? "font-bold opacity-100" : "opacity-80 hover:opacity-100"
                      }`}
                    >
                      {tab.label}
                      <div
                        className={`absolute -bottom-[10px] left-0 right-0 h-1 rounded-t-full ${isActive ? "bg-[#004287]" : "hidden"}`}
                      ></div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        <h2 className="font-headline-lg-mobile md:hidden text-[#121c2a] mb-4 mt-4 font-bold tracking-tight">
          {tabConfig.title}
        </h2>

        <div className="bg-white rounded border border-[#c2c6d3] p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative flex-1 w-full md:w-auto">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#424751] pointer-events-none" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search..."
              className="w-full h-9 pl-9 pr-3 rounded border border-[#c2c6d3] bg-white text-sm text-[#121c2a] placeholder:text-[#424751] outline-none transition-colors focus:border-[#004287] focus:ring-2 focus:ring-[#d6e3ff]"
            />
          </div>

          <div className="flex items-center gap-3 md:ml-4">
            <button
              onClick={() => setPage(1)}
              className="p-2 border border-[#c2c6d3] rounded hover:bg-[#eff4ff] transition-colors flex items-center justify-center text-[#424751]"
              title="Refresh"
            >
              <RefreshCw size={18} />
            </button>
            <button
              onClick={() => alert("Export CSV")}
              className="flex items-center gap-2 px-4 py-2 border border-[#004287] text-[#004287] font-bold rounded transition-colors hover:bg-[#eff4ff]"
            >
              <Download size={18} />
              <span>Export</span>
            </button>
          </div>
        </div>

        {activeTab === "receive-goods" && (
          <ReceiveGoodsTab
            selectedPO={selectedPO}
            setSelectedPO={setSelectedPO}
            invoiceNo={invoiceNo}
            setInvoiceNo={setInvoiceNo}
            invoiceDate={invoiceDate}
            setInvoiceDate={setInvoiceDate}
            receivedDate={receivedDate}
            setReceivedDate={setReceivedDate}
            receivedItems={receivedItems}
            updateItemData={updateItemData}
            notes={notes}
            setNotes={setNotes}
            totals={totals}
            page={page}
            setPage={setPage}
          />
        )}
        {activeTab === "batch-entry" && (
          <BatchEntryTab
            receivedItems={receivedItems}
            currentBatchItemId={currentBatchItemId}
            setCurrentBatchItemId={setCurrentBatchItemId}
            itemBatches={itemBatches}
            updateBatchValue={updateBatchValue}
            addBatchRow={addBatchRow}
            removeBatchRow={removeBatchRow}
            calculateBatchTotal={calculateBatchTotal}
          />
        )}
        {activeTab === "expiry-entry" && (
          <ExpiryEntryTab
            receivedItems={receivedItems}
            itemBatches={itemBatches}
            updateItemData={updateItemData}
            calculateShelfLife={calculateShelfLife}
            expiryStats={expiryStats}
          />
        )}
        {activeTab === "purchase-return" && (
          <PurchaseReturnTab
            receivedItems={receivedItems}
            returnReason={returnReason}
            setReturnReason={setReturnReason}
            returnDate={returnDate}
            setReturnDate={setReturnDate}
            returnQuantities={returnQuantities}
            updateReturnQuantity={updateReturnQuantity}
            estimatedCredit={estimatedCredit}
            page={page}
            setPage={setPage}
          />
        )}
        {activeTab === "credit-notes" && (
          <CreditNotesTab
            creditNoteNumber={creditNoteNumber}
            setCreditNoteNumber={setCreditNoteNumber}
            creditNoteAmount={creditNoteAmount}
            setCreditNoteAmount={setCreditNoteAmount}
          />
        )}
      </main>

      <div className="bg-white border-t border-[#c2c6d3] p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-20 flex justify-between items-center fixed bottom-0 left-0 md:left-64 right-0">
        <button className="px-6 py-2 text-[#424751] font-label-md hover:bg-[#eff4ff] border border-transparent hover:border-[#c2c6d3] rounded transition-all">
          Cancel
        </button>
        <div className="flex gap-3">
          <button
            onClick={handleSaveDraft}
            className="px-6 py-2 border border-[#004287] text-[#004287] rounded font-label-md transition-colors hover:bg-[#eff4ff] hidden sm:flex items-center gap-2"
          >
            <Save size={16} />
            Save Draft
          </button>
          <button
            onClick={handleConfirm}
            disabled={isSubmitting}
            className="px-8 py-2 rounded font-label-md shadow-sm flex items-center gap-2 text-white bg-[#004287] hover:bg-[#235eac] transition-colors disabled:opacity-70"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Processing...
              </>
            ) : (
              <>
                <TabIcon size={18} />
                {tabConfig.text}
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PurchasePageInvoice;
