import { useState } from "react";
import { staffMembers } from "../../../data/staffManagement/staffData";
import api, { getActivePharmacyId } from "../../../services/api";
import KioskCard from "../../../components/staffManagement/kiosk/KioskCard";
import KioskFooter from "../../../components/staffManagement/kiosk/KioskFooter";
import LiveClock from "../../../components/staffManagement/kiosk/LiveClock";

export default function Kiosk() {
  const [employeeId,setEmployeeId]=useState(""); const [confirmedEmployee,setConfirmedEmployee]=useState(null); const [timestamp,setTimestamp]=useState(""); const [status,setStatus]=useState(""); const [isProcessing,setIsProcessing]=useState(false);
  const handleAction=async(actionType)=>{ if(!employeeId.trim()) return; setIsProcessing(true); setStatus(""); const employee=staffMembers.find(x=>String(x.employee_code||x.id).toLowerCase()===employeeId.trim().toLowerCase()); if(!employee){setConfirmedEmployee(null);setStatus("Employee not found. Please verify the ID.");setIsProcessing(false);return;} try{const pharmacyId=getActivePharmacyId(); if(!pharmacyId) throw new Error("Active pharmacy is unavailable"); const url=`/pharmacies/${pharmacyId}/staff/${employee.id}/${actionType==="check-in"?"check-in":"check-out"}`; const {data}=await api.post(url,{notes:"Kiosk attendance"}); setConfirmedEmployee(employee); setTimestamp(new Date(data.check_in_at||data.check_out_at||Date.now()).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})); setStatus(actionType==="check-in"?"Checked in successfully":"Checked out successfully"); }catch(e){setStatus(e?.response?.data?.detail||e.message||"Attendance action failed");}finally{setIsProcessing(false);}};
  return <div className="flex h-full flex-col"><div className="relative flex flex-1 flex-col items-center justify-center overflow-hidden p-8"><KioskCard employeeId={employeeId} onEmployeeIdChange={setEmployeeId} onCheckIn={()=>handleAction("check-in")} onCheckOut={()=>handleAction("check-out")} isProcessing={isProcessing} confirmedEmployee={confirmedEmployee} timestamp={timestamp} status={status}/><LiveClock/></div><KioskFooter/></div>;
}
