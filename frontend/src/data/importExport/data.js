export let tabData={};
export let importHistory=[];
export let exportColumns=["SKU","Name","Category","Batch No.","Expiry Date","Quantity","Unit Price","Supplier ID","Status"];
export function setRuntimeData(d){tabData=d.tabData||{};importHistory=d.importHistory||[];exportColumns=d.exportColumns||exportColumns;}
export function clearRuntimeData(){setRuntimeData({});}
