import { useEffect, useMemo, useState } from "react";
import SupplierHeader from "../../components/supplierManagement/suppliers/SupplierHeader";
import SupplierCard from "../../components/supplierManagement/suppliers/SupplierCard";
import SupplierModal from "../../components/supplierManagement/suppliers/SupplierModal";
import { supplierData, setRuntimeData } from "../../data/reports/mockData";
import api, { withPharmacy } from "../../services/api";

const emptyForm = () => ({
  name: "", contactPerson: "", email: "", phone: "", category_id: "",
  address: "", paymentTerms: "", gstin: "", drugLicense: "",
  bankName: "", accountNumber: "", ifscCode: "", status: "active", description: ""
});
export let initialSuppliersData = supplierData;

const Suppliers = () => {
  const [suppliers, setSuppliers] = useState(supplierData);
  const [categories, setCategories] = useState([]);
  const [selectedSupplier, setSelectedSupplier] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const loadCategories = async () => {
    try {
      const { data } = await api.get("/catalog", { params: { ...withPharmacy(), option_type: "supplier_category" } });
      setCategories(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Unable to load supplier categories", e);
      setCategories([]);
    }
  };

  useEffect(() => { loadCategories(); }, []);

  const defaultCategory = useMemo(() => categories[0]?.id || "", [categories]);

  const normalize = (s) => ({
    ...s,
    contactPerson: s.contact_person ?? s.contactPerson ?? "",
    paymentTerms: s.payment_terms ?? s.paymentTerms ?? "",
    drugLicense: s.drug_license ?? s.drugLicense ?? "",
    bankName: s.bank_name ?? s.bankName ?? "",
    accountNumber: s.account_number ?? s.accountNumber ?? "",
    ifscCode: s.ifsc_code ?? s.ifscCode ?? "",
    category_id: s.category_id ?? "",
    category: s.category_name ?? s.category ?? "Uncategorized",
    status: s.status || "active",
  });

  const refresh = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/suppliers", { params: withPharmacy() });
      const rows = (data || []).map(normalize);
      setSuppliers(rows);
      initialSuppliersData = rows;
      setRuntimeData({ supplierData: rows });
    } finally { setLoading(false); }
  };

  useEffect(() => { refresh().catch(console.error); }, []);

  const handleOpenAdd = () => {
    setSelectedSupplier(null);
    setIsAddModalOpen(true);
  };

  const handleOpenEdit = (supplier) => {
    const s = normalize(supplier);
    setSelectedSupplier(s);
    setFormData({
      name: s.name || "", contactPerson: s.contactPerson, email: s.email || "",
      phone: s.phone || "", category_id: s.category_id || defaultCategory,
      address: s.address || "", paymentTerms: s.paymentTerms || "",
      gstin: s.gstin || "", drugLicense: s.drugLicense || "",
      bankName: s.bankName || "", accountNumber: s.accountNumber || "",
      ifscCode: s.ifscCode || "", status: s.status || "active", description: s.description || ""
    });
    setIsEditModalOpen(true);
  };

  const [formData, setFormData] = useState(emptyForm());

  useEffect(() => {
    if (isAddModalOpen) setFormData({ ...emptyForm(), category_id: defaultCategory });
  }, [isAddModalOpen, defaultCategory]);

  const payload = () => ({
    name: formData.name.trim(),
    contact_person: formData.contactPerson.trim() || null,
    email: formData.email.trim() || null,
    phone: formData.phone.trim() || null,
    category_id: formData.category_id || null,
    address: formData.address.trim() || null,
    payment_terms: formData.paymentTerms.trim() || null,
    gstin: formData.gstin.trim() || null,
    drug_license: formData.drugLicense.trim() || null,
    bank_name: formData.bankName.trim() || null,
    account_number: formData.accountNumber.trim() || null,
    ifsc_code: formData.ifscCode.trim() || null,
    status: formData.status,
    description: formData.description.trim() || null,
  });

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    try {
      await api.patch(`/suppliers/${selectedSupplier.id}`, payload(), { params: withPharmacy() });
      setIsEditModalOpen(false); await refresh();
    } catch (error) { alert(error?.response?.data?.detail || "Unable to update supplier"); }
  };

  const handleAddSupplier = async (e) => {
    e.preventDefault();
    try {
      await api.post("/suppliers", payload(), { params: withPharmacy() });
      setIsAddModalOpen(false); await refresh();
    } catch (error) { alert(error?.response?.data?.detail || "Unable to create supplier"); }
  };

  return (
    <div className="space-y-6 pb-12">
      <SupplierHeader onAddClick={handleOpenAdd} />
      <div className="text-xs text-on-surface-variant">{loading ? "Refreshing supplier directory…" : `${suppliers.length} supplier(s) • categories controlled by Medorax Admin`}</div>
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {suppliers.map((supplier) => <SupplierCard key={supplier.id} supplier={normalize(supplier)} onEditClick={handleOpenEdit} />)}
      </div>
      <SupplierModal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)} title="Manage Supplier Profile" subtitle="Update supplier master data, category, banking and payment terms." onSubmit={handleSaveEdit} formData={formData} setFormData={setFormData} submitLabel="Save Changes" categories={categories} />
      <SupplierModal isOpen={isAddModalOpen} onClose={() => setIsAddModalOpen(false)} title="Add New Supplier" subtitle="Register a supplier against the active pharmacy database." onSubmit={handleAddSupplier} formData={formData} setFormData={setFormData} submitLabel="Add Supplier" categories={categories} />
    </div>
  );
};

export default Suppliers;
