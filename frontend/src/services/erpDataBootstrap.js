import api, { setActivePharmacyId, withPharmacy } from "./api";
import * as inventoryData from "../data/inventoryManagement/inventoryData";
import * as pharmacyData from "../data/pharmacySettings/pharmacySettingsData";
import * as purchaseData from "../data/purchases/data";
import * as billingData from "../data/billing/billingData";
import * as importExportData from "../data/importExport/data";
import * as reportMockData from "../data/reports/mockData";
import * as staffAttendance from "../data/staffManagement/attendanceData";
import * as staffActivity from "../data/staffManagement/activityLogsData";
import * as staffData from "../data/staffManagement/staffData";

const money = (value) => `₹${Number(value || 0).toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
const fmtDate = (value) => value ? new Date(value).toLocaleString("en-IN") : "—";

const flattenBatches = (medicines = []) => medicines.flatMap((m) =>
  (m.batches || []).map((b) => ({
    id: b.id,
    medicineId: m.id,
    name: m.name,
    sku: m.sku || "—",
    category: m.category || "Uncategorized",
    batch: b.batch_number,
    quantity: Number(b.quantity_available || 0),
    unit: m.unit || "Units",
    expiry: b.expiry_date,
    purchasePrice: Number(b.purchase_price || 0),
    sellingPrice: Number(b.selling_price || 0),
    mrp: Number(b.mrp || 0),
    status: b.status,
    location: m.rack || "—",
    lastUpdated: fmtDate(m.updated_at || b.updated_at),
  }))
);

export async function loadERPData() {
  const pharmaciesResponse = await api.get("/pharmacies/mine");
  const pharmacies = pharmaciesResponse.data || [];
  if (!pharmacies.length) throw new Error("No pharmacy is associated with this ERP account.");

  const storedId = localStorage.getItem("medorax.erp.pharmacy_id");
  const pharmacy = pharmacies.find((p) => p.id === storedId) || pharmacies[0];
  setActivePharmacyId(pharmacy.id);

  const q = withPharmacy();
  // Pull pharmacy-scoped master data from Medorax Admin before loading forms.
  // The ERP backend authenticates the request with its installed signed license.
  try {
    await api.post("/admin-sync/catalog", null, { params: q });
  } catch (error) {
    console.warn("[ERP bootstrap] Admin catalog sync unavailable; using local catalog cache.", error?.response?.data || error?.message);
  }

  const requests = [
    ["catalog", api.get("/catalog", { params: q })],
    ["dashboard", api.get("/reports/dashboard", { params: q })],
    ["sales", api.get("/reports/sales", { params: q })],
    ["expiry", api.get("/reports/expiry", { params: { ...q, days_ahead: 60 } })],
    ["medicines", api.get("/medicines", { params: q })],
    ["suppliers", api.get("/suppliers", { params: q })],
    ["purchases", api.get("/purchases", { params: q })],
    ["branches", api.get(`/pharmacies/${pharmacy.id}/branches`, { params: { limit: 500 } })],
    ["staff", api.get(`/pharmacies/${pharmacy.id}/staff`, { params: { limit: 500 } })],
    ["attendance", api.get(`/pharmacies/${pharmacy.id}/attendance`, { params: { limit: 500 } })],
    ["settings", api.get("/settings", { params: q })],
    ["notifications", api.get("/notifications", { params: { ...q, limit: 100 } })],
    ["auditLogs", api.get("/audit-logs", { params: { ...q, limit: 100 } })],
    ["customers", api.get("/api/customers/", { params: { pharmacy_id: pharmacy.id } })],
    ["ledger", api.get("/inventory/ledger", { params: q })],
  ];

  const results = await Promise.allSettled(requests.map(([, request]) => request));

  results.forEach((result, index) => {
    if (result.status === "rejected") {
      console.error(
        `[ERP bootstrap] ${requests[index][0]} failed:`,
        result.reason?.response?.status,
        result.reason?.response?.data || result.reason?.message || result.reason
      );
    }
  });

  const value = (i, fallback) => {
    const result = results[i];

    if (!result) {
      return fallback;
    }

    return result.status === "fulfilled"
      ? result.value?.data ?? fallback
      : fallback;
  };
  const catalog = value(0, []);
  const dashboard = value(1, {});
  const sales = value(2, []);
  const expiry = value(3, []);
  const medicines = value(4, []);
  const suppliers = value(5, []);
  const purchases = value(6, []);
  const branches = value(7, []);
  const staff = value(8, []);
  const attendance = value(9, []);
  const settings = value(10, {});
  const notifications = value(11, []);
  const auditLogs = value(12, []);
  const customers = value(13, { stats: {}, rows: [] });
  const ledger = value(14, []);

  const batches = flattenBatches(medicines);
  const branchName = (id) => branches.find((b) => b.id === id)?.name || "—";
  const stockByMedicine = medicines.map((m) => {
    const bs = m.batches || [];
    const quantity = bs.reduce((sum, b) => sum + Number(b.quantity_available || 0), 0);
    return {
      id: m.id, name: m.name, sku: m.sku || "—", category: m.category || "Uncategorized",
      quantity, unit: m.unit || "Units", location: m.rack || "—",
      status: quantity <= Number(m.min_stock_level || 0) ? (quantity ? "Low Stock" : "Out of Stock") : "In Stock",
      lastUpdated: fmtDate(m.updated_at),
    };
  });

  const lowStock = stockByMedicine.filter((m) => m.status !== "In Stock");

  inventoryData.setRuntimeData({
    currentStockItems: stockByMedicine,
    openingStockItems: [], closingStockItems: [],
    availableStockItems: stockByMedicine.map((m) => ({ ...m, totalQty: m.quantity, reservedQty: 0, availableQty: m.quantity, status: m.quantity ? "Available" : "Out of Stock" })),
    reservedStockItems: [], batchItems: batches,
    stockAdjustmentItems: ledger.filter((x) => x.transaction_type === "ADJUSTMENT"), stockTransferItems: [], physicalVerificationItems: [], damagedStockItems: [],
    expiredStockItems: expiry.filter((x) => x.status === "Expired"),
    nearExpiryItems: expiry.filter((x) => x.status !== "Expired"),
    lowStockItems: lowStock,
    categories: catalog.filter((x) => x.option_type === "medicine_category").map((x) => x.name),
    warehouses: branches.map((b) => b.name),
    overstockItems: [], stockLedgerItems: ledger,
  });

  pharmacyData.setRuntimeData({
    kpiSummary: [
      { id: "todays-sales", label: "Today's Sales", value: money(dashboard.today_sales), icon: "payments" },
      { id: "total-orders", label: "Total Orders", value: sales.length.toLocaleString("en-IN"), icon: "shopping-bag" },
      { id: "active-branches", label: "Active Branches", value: branches.filter((b) => b.is_active).length.toLocaleString("en-IN"), icon: "building-2" },
      { id: "low-stock", label: "Low Stock", value: String(dashboard.low_stock_count || lowStock.length), icon: "alert-triangle", accent: "error" },
    ],
    revenueOverview: { periods: ["Monthly"], bars: [Number(dashboard.monthly_sales || 0)] },
    branchPerformance: branches.map((b) => ({ name: b.name, score: b.is_active ? 100 : 0 })),
    categoryDistribution: { totalSkus: medicines.length.toLocaleString("en-IN"), categories: [...new Set(medicines.map((m) => m.category).filter(Boolean))].map((name) => ({ name })) },
    recentOrders: sales.slice(0, 10).map((x) => ({ orderId: x.invoice_number, customer: x.customer_name || "Walk-in", branch: branchName(x.branch_id), amount: money(x.total_amount), status: x.status })),
    quickActions: [],
    lowStockAlerts: lowStock.slice(0, 10).map((m) => ({ medicine: m.name, location: m.location, quantity: m.quantity })),
    recentActivity: auditLogs.slice(0, 10).map((x) => ({ title: x.action_type, detail: x.entity_type || "", meta: `${fmtDate(x.created_at)} • ${x.user_email || "System"}`, tone: "neutral", icon: "activity" })),
    pharmacyProfile: { business: { pharmacyName: pharmacy.name, gstNumber: pharmacy.gst_number, panNumber: pharmacy.pan_number, address: pharmacy.address, contactPhone: pharmacy.contact_phone, contactEmail: pharmacy.contact_email }, owner: {}, address: {}, license: {} },
    branches,
    directorySummary: { total: branches.length },
    directoryBranches: branches,
    branchDeepDive: branches,
  });

  billingData.setRuntimeData({
    suggestedProducts: medicines.flatMap((m) => (m.batches || []).slice(0, 1).map((b) => ({ id: m.id, name: m.name, sku: m.sku || "—", price: Number(b.selling_price || b.mrp || 0), stock: Number(b.quantity_available || 0), available: Number(b.quantity_available || 0) > 0, batch_number: b.batch_number, gst_percentage: Number(m.gst_percentage || 0) }))),
    initialCartItems: [],
    quickProducts: medicines.map((m) => ({ id: m.id, name: m.name, price: Number(m.batches?.[0]?.selling_price || m.batches?.[0]?.mrp || 0), category: m.category || "Medicine" })),
  });

  purchaseData.setRuntimeData({
    initialReceivedItems: [], poOptions: purchases.map((p) => ({ id: p.id, label: p.invoice_number })), creditNotes: [], returnReasons: [], initialOrderItems: [],
    productOptions: medicines.map((m) => ({ id: m.id, name: m.name, sku: m.sku || "—", price: Number(m.batches?.[0]?.purchase_price || 0) })),
    unitOptions: [...new Set(medicines.map((m) => m.unit).filter(Boolean))], taxOptions: [...new Set(medicines.map((m) => String(m.gst_percentage ?? "0")))],
    supplierOptions: suppliers.map((s) => ({ id: s.id, name: s.name })),
    locationOptions: branches.map((b) => ({ id: b.id, name: b.name })),
    productOptions: medicines.map((m) => ({ id: m.id, name: m.name, sku: m.sku || "", price: Number(m.batches?.[0]?.purchase_price || 0) })),
    initialOrderItems: [],
    initialReceivedItems: [],
    poOptions: purchases.map((p) => ({ id: p.id, label: p.invoice_number, status: p.status })),
  });

  importExportData.setRuntimeData({ tabData: {}, importHistory: [], exportColumns: ["SKU", "Name", "Category", "Batch No.", "Expiry Date", "Quantity", "Unit Price", "Supplier ID", "Status"] });
  reportMockData.setRuntimeData({
    salesData: sales, profitData: [], purchaseData: purchases, inventoryData: batches, gstData: [], customerData: customers.rows || [], supplierData: suppliers.map((x) => ({ ...x, contactPerson: x.contact_person, paymentTerms: x.payment_terms, balance: money(x.outstanding_balance), totalOrders: 0, status: "Active" })),
  });
  staffAttendance.setRuntimeData(attendance.map((a) => ({ ...a, name: staff.find((s) => s.id === a.staff_id)?.first_name || a.staff_id, date: fmtDate(a.check_in_at), checkIn: fmtDate(a.check_in_at), checkOut: fmtDate(a.check_out_at), workingHours: a.working_minutes != null ? `${(a.working_minutes / 60).toFixed(1)} hrs` : "—", status: a.check_out_at ? "Present" : "Open" })));
  staffActivity.setRuntimeData(auditLogs);
  staffData.setRuntimeData(staff);

  return { pharmacy, branches, medicines, suppliers, purchases, staff, attendance, settings, notifications, auditLogs, dashboard, sales, expiry, customers, ledger };
}

export function clearERPData() {
  inventoryData.clearRuntimeData();
  pharmacyData.clearRuntimeData();
  purchaseData.clearRuntimeData();
  billingData.clearRuntimeData();
  importExportData.clearRuntimeData();
  reportMockData.clearRuntimeData();
  staffAttendance.setRuntimeData([]);
  staffActivity.setRuntimeData([]);
  staffData.clearRuntimeData();
}
