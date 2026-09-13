export let suggestedProducts = [];
export let initialCartItems = [];
export let quickProducts = [];
export function setRuntimeData(data){ suggestedProducts=data.suggestedProducts||[]; initialCartItems=data.initialCartItems||[]; quickProducts=data.quickProducts||[]; }
export function clearRuntimeData(){setRuntimeData({});}
