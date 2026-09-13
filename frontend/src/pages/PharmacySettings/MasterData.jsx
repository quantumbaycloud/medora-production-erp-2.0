import { useEffect, useState } from "react";
import { RefreshCw, ShieldCheck } from "lucide-react";
import api, { withPharmacy } from "../../services/api";

const TYPES=[["supplier_category","Supplier Categories"],["medicine_category","Medicine Categories"],["payment_term","Payment Terms"],["customer_type","Customer Types"],["dosage_form","Dosage Forms"],["unit","Units"]];

export default function MasterData(){
 const [items,setItems]=useState([]),[type,setType]=useState("supplier_category"),[loading,setLoading]=useState(false);
 const load=async()=>{setLoading(true);try{const {data}=await api.get("/catalog",{params:{...withPharmacy(),option_type:type}});setItems(data||[])}catch(e){console.error(e)}finally{setLoading(false)}};
 useEffect(()=>{load()},[type]);
 return <div className="space-y-6">
  <div><h1 className="text-2xl font-bold text-on-background">Master Data</h1><p className="mt-1 text-sm text-on-surface-variant">Pharmacy-specific options are controlled by Medorax Admin and synchronized to this licensed ERP.</p></div>
  <div className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-5 flex flex-col md:flex-row gap-3 md:items-center">
   <select value={type} onChange={e=>setType(e.target.value)} className="rounded-xl border border-outline-variant p-3 bg-white">{TYPES.map(([v,l])=><option key={v} value={v}>{l}</option>)}</select>
   <button onClick={load} className="inline-flex items-center gap-2 rounded-xl border border-outline-variant px-4 py-3 text-sm font-semibold"><RefreshCw size={16} className={loading?"animate-spin":""}/> Refresh</button>
   <span className="ml-auto inline-flex items-center gap-2 text-xs text-on-surface-variant"><ShieldCheck size={15}/> Admin synchronized</span>
  </div>
  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{items.map(x=><div key={x.id} className="rounded-xl border border-outline-variant bg-surface-container-lowest p-4"><div className="font-semibold">{x.name}</div><div className="mt-1 text-xs font-mono text-outline">{x.code}</div></div>)}{!loading&&!items.length&&<div className="col-span-full rounded-xl border border-dashed border-outline-variant p-10 text-center text-sm text-on-surface-variant">No options have been configured by Admin yet.</div>}</div>
 </div>
}
