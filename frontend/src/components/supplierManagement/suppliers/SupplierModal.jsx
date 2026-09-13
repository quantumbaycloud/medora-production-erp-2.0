import { X } from "lucide-react";

const SupplierModal = ({ isOpen, onClose, title, subtitle, onSubmit, formData, setFormData, submitLabel, categories = [] }) => {
  if (!isOpen) return null;
  const set = (key, value) => setFormData({ ...formData, [key]: value });
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
      <div className="w-full max-w-2xl rounded-2xl bg-surface-container-lowest p-6 shadow-2xl my-8">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div><h2 className="text-lg font-bold text-on-background">{title}</h2><p className="text-xs text-on-surface-variant">{subtitle}</p></div>
          <button type="button" onClick={onClose} className="rounded-lg p-1.5 text-outline hover:bg-surface-container"><X size={18}/></button>
        </div>
        <form onSubmit={onSubmit} className="mt-4 space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="Company / Supplier Name *"><input required value={formData.name||""} onChange={e=>set("name",e.target.value)} className={input}/></Field>
            <Field label="Contact Person"><input value={formData.contactPerson||""} onChange={e=>set("contactPerson",e.target.value)} className={input}/></Field>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="Supplier Category *"><select required value={formData.category_id||""} onChange={e=>set("category_id",e.target.value)} className={input+" bg-surface-container-lowest"}><option value="">Select category</option>{categories.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></Field>
            <Field label="Status"><select value={formData.status||"active"} onChange={e=>set("status",e.target.value)} className={input+" bg-surface-container-lowest"}><option value="active">Active</option><option value="inactive">Inactive</option><option value="on_hold">On Hold</option></select></Field>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="Email"><input type="email" value={formData.email||""} onChange={e=>set("email",e.target.value)} className={input}/></Field>
            <Field label="Phone"><input value={formData.phone||""} onChange={e=>set("phone",e.target.value)} className={input}/></Field>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="GSTIN / Tax ID"><input value={formData.gstin||""} onChange={e=>set("gstin",e.target.value.toUpperCase())} className={input+" font-mono"}/></Field>
            <Field label="Drug License"><input value={formData.drugLicense||""} onChange={e=>set("drugLicense",e.target.value)} className={input}/></Field>
          </div>
          <Field label="Address"><input value={formData.address||""} onChange={e=>set("address",e.target.value)} className={input}/></Field>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <Field label="Bank Name"><input value={formData.bankName||""} onChange={e=>set("bankName",e.target.value)} className={input}/></Field>
            <Field label="Account Number"><input value={formData.accountNumber||""} onChange={e=>set("accountNumber",e.target.value)} className={input}/></Field>
            <Field label="IFSC"><input value={formData.ifscCode||""} onChange={e=>set("ifscCode",e.target.value.toUpperCase())} className={input+" font-mono"}/></Field>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="Payment Terms"><input placeholder="e.g. Net 30" value={formData.paymentTerms||""} onChange={e=>set("paymentTerms",e.target.value)} className={input}/></Field>
            <Field label="Description / Notes"><input value={formData.description||""} onChange={e=>set("description",e.target.value)} className={input}/></Field>
          </div>
          <div className="pt-3 flex justify-end gap-2 border-t border-slate-100">
            <button type="button" onClick={onClose} className="rounded-xl border border-outline-variant px-4 py-2 font-semibold text-on-surface-variant">Cancel</button>
            <button type="submit" className="rounded-xl bg-primary px-5 py-2 font-semibold text-on-primary shadow-sm">{submitLabel}</button>
          </div>
        </form>
      </div>
    </div>
  );
};
const input="w-full rounded-xl border border-outline-variant p-2.5 outline-none focus:border-primary";
const Field=({label,children})=><div><label className="block font-semibold text-on-surface-variant mb-1">{label}</label>{children}</div>;
export default SupplierModal;
