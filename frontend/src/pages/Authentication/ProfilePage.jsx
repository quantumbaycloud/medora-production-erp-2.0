import { useEffect, useState } from "react";
import { Mail, Phone, UserCircle } from "lucide-react";
import api from "../../services/api";

export default function ProfilePage() {
  const [user, setUser] = useState(null);
  const [name, setName] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  useEffect(() => { api.get("/auth/me").then(({ data }) => { const u=data?.user||data; setUser(u); setName(u?.name||""); localStorage.setItem("user", JSON.stringify(u)); }).catch(() => {}); }, []);
  const save = async (e) => { e.preventDefault(); setSaving(true); setMessage(""); try { const {data}=await api.patch("/users/me", {name}); setUser(data); localStorage.setItem("user", JSON.stringify(data)); setMessage("Profile updated successfully."); } catch(e) { setMessage(e?.response?.data?.detail || "Unable to update profile."); } finally { setSaving(false); } };
  if (!user) return <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-8">Loading profile…</div>;
  return <div className="mx-auto max-w-3xl space-y-6"><div><h1 className="text-2xl font-bold">My Profile</h1><p className="mt-1 text-sm text-on-surface-variant">Manage the authenticated ERP account provided by MEDORAX onboarding.</p></div><div className="rounded-2xl border border-outline-variant bg-surface-container-lowest p-6"><div className="mb-6 flex items-center gap-4"><div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-xl font-bold text-on-primary">{(name||user.username||"U").slice(0,1).toUpperCase()}</div><div><h2 className="text-lg font-semibold">{user.name||user.username}</h2><p className="text-sm text-on-surface-variant">{user.username||""}</p></div></div><form onSubmit={save} className="space-y-4"><label className="block text-sm font-medium">Full name<input value={name} onChange={e=>setName(e.target.value)} className="mt-1.5 w-full rounded-lg border border-outline-variant bg-surface-container-low px-3 py-2.5" required /></label><div className="grid gap-4 sm:grid-cols-2"><div className="rounded-lg bg-surface-container-low p-3 text-sm"><Mail size={16} className="mb-1 text-primary" />{user.email||"No email"}</div><div className="rounded-lg bg-surface-container-low p-3 text-sm"><Phone size={16} className="mb-1 text-primary" />{user.phone||"No mobile number"}</div></div>{message&&<p className="text-sm text-primary">{message}</p>}<button disabled={saving} className="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-on-primary disabled:opacity-60">{saving?"Saving…":"Save profile"}</button></form></div></div>;
}
