export let initialReceivedItems = [];
export let poOptions = [];
export let purchaseData = [];
export let creditNotes = [];
export let returnReasons = [];
export let initialOrderItems = [];
export let productOptions = [];
export let unitOptions = [];
export let taxOptions = [];
export let supplierOptions = [];
export let locationOptions = [];

export function setRuntimeData(d = {}) {
  initialReceivedItems = d.initialReceivedItems || [];
  poOptions = d.poOptions || [];
  purchaseData = d.purchaseData || [];
  creditNotes = d.creditNotes || [];
  returnReasons = d.returnReasons || [];
  initialOrderItems = d.initialOrderItems || [];
  productOptions = d.productOptions || [];
  unitOptions = d.unitOptions || [];
  taxOptions = d.taxOptions || [];
  supplierOptions = d.supplierOptions || [];
  locationOptions = d.locationOptions || [];
}

export function clearRuntimeData() {
  setRuntimeData({});
}