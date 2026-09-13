import api, { getActivePharmacyId, withPharmacy } from "./api";

const pharmacyParams = (params = {}) => withPharmacy(params);

const downloadResponse = async (request, fallbackName = "medorax-export") => {
  const response = await request;
  const disposition = response.headers?.["content-disposition"] || "";
  const match = disposition.match(/filename="?([^";]+)"?/i);
  const filename = match?.[1] || fallbackName;
  const blob = new Blob([response.data], { type: response.headers?.["content-type"] || "application/octet-stream" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  return filename;
};

export const erpApi = {
  pharmacyId: () => getActivePharmacyId(),
  medicines: (q = "") => api.get("/medicines", { params: pharmacyParams(q ? { q } : {}) }),
  createMedicine: (payload) => api.post("/medicines", payload, { params: pharmacyParams() }),
  updateMedicine: (id, payload) => api.patch(`/medicines/${id}`, payload, { params: pharmacyParams() }),
  medicineBatches: (id) => api.get(`/medicines/${id}/batches`, { params: pharmacyParams() }),
  createMedicineBatch: (id, payload) => api.post(`/medicines/${id}/batches`, payload, { params: pharmacyParams() }),
  suppliers: (params = {}) => api.get("/suppliers", { params: pharmacyParams(params) }),
  createSupplier: (payload) => api.post("/suppliers", payload, { params: pharmacyParams() }),
  updateSupplier: (id, payload) => api.patch(`/suppliers/${id}`, payload, { params: pharmacyParams() }),
  deleteSupplier: (id) => api.delete(`/suppliers/${id}`, { params: pharmacyParams() }),
  customers: (params = {}) => api.get("/api/customers/", { params: pharmacyParams(params) }),
  createCustomer: (payload) => api.post("/api/customers/", payload, { params: pharmacyParams() }),
  purchases: (params = {}) => api.get("/purchases", { params: pharmacyParams(params) }),
  createPurchase: (payload) => api.post("/purchases", payload, { params: pharmacyParams() }),
  updatePurchase: (id, payload) => api.patch(`/purchases/${id}`, payload, { params: pharmacyParams() }),
  approvePurchase: (id) => api.post(`/purchases/${id}/approve`, null, { params: pharmacyParams() }),
  inventoryLedger: (params = {}) => api.get("/inventory/ledger", { params: pharmacyParams(params) }),
  adjustInventory: (payload, branchId = null) => api.post("/inventory/adjust", payload, { params: pharmacyParams(branchId ? { branch_id: branchId } : {}) }),
  staff: (pharmacyId, params = {}) => api.get(`/pharmacies/${pharmacyId}/staff`, { params }),
  attendance: (pharmacyId, params = {}) => api.get(`/pharmacies/${pharmacyId}/attendance`, { params }),
  auditLogs: (params = {}) => api.get("/audit-logs", { params: pharmacyParams(params) }),
  dashboard: (params = {}) => api.get("/reports/dashboard", { params: pharmacyParams(params) }),
  salesReport: (params = {}) => api.get("/reports/sales", { params: pharmacyParams(params) }),
  expiryReport: (params = {}) => api.get("/reports/expiry", { params: pharmacyParams(params) }),
  gstReport: (params = {}) => api.get("/reports/gst", { params: pharmacyParams(params) }),
  settings: (params = {}) => api.get("/settings", { params: pharmacyParams(params) }),
  updateSettings: (payload) => api.patch("/settings", payload, { params: pharmacyParams() }),
  exportEntity: (entity, format = "csv") => downloadResponse(api.get(`/inventory/export/${encodeURIComponent(entity)}`, { params: pharmacyParams({ format }), responseType: "blob" }), `medorax-${entity}.${format === "excel" ? "xlsx" : format}`),
  importMedicines: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.post("/inventory/import/medicines", form, { params: pharmacyParams(), headers: { "Content-Type": "multipart/form-data" } });
  },
};

export default erpApi;
