export let currentStockItems = [];
export let openingStockItems = [];
export let closingStockItems = [];
export let availableStockItems = [];
export let reservedStockItems = [];
export let batchItems = [];
export let stockAdjustmentItems = [];
export let stockTransferItems = [];
export let physicalVerificationItems = [];
export let damagedStockItems = [];
export let expiredStockItems = [];
export let nearExpiryItems = [];
export let lowStockItems = [];
export let categories = [];
export let warehouses = [];
export let overstockItems = [];
export let stockLedgerItems = [];

export function setRuntimeData(data = {}) {
  for (const key of ["currentStockItems","openingStockItems","closingStockItems","availableStockItems","reservedStockItems","batchItems","stockAdjustmentItems","stockTransferItems","physicalVerificationItems","damagedStockItems","expiredStockItems","nearExpiryItems","lowStockItems","categories","warehouses","overstockItems","stockLedgerItems"]) {
    if (Object.prototype.hasOwnProperty.call(data, key)) {
      if (key === "currentStockItems") currentStockItems = data[key];
      else if (key === "openingStockItems") openingStockItems = data[key];
      else if (key === "closingStockItems") closingStockItems = data[key];
      else if (key === "availableStockItems") availableStockItems = data[key];
      else if (key === "reservedStockItems") reservedStockItems = data[key];
      else if (key === "batchItems") batchItems = data[key];
      else if (key === "stockAdjustmentItems") stockAdjustmentItems = data[key];
      else if (key === "stockTransferItems") stockTransferItems = data[key];
      else if (key === "physicalVerificationItems") physicalVerificationItems = data[key];
      else if (key === "damagedStockItems") damagedStockItems = data[key];
      else if (key === "expiredStockItems") expiredStockItems = data[key];
      else if (key === "nearExpiryItems") nearExpiryItems = data[key];
      else if (key === "lowStockItems") lowStockItems = data[key];
      else if (key === "categories") categories = data[key];
      else if (key === "warehouses") warehouses = data[key];
      else if (key === "overstockItems") overstockItems = data[key];
      else if (key === "stockLedgerItems") stockLedgerItems = data[key];
    }
  }
}
export function clearRuntimeData(){ setRuntimeData({currentStockItems:[],openingStockItems:[],closingStockItems:[],availableStockItems:[],reservedStockItems:[],batchItems:[],stockAdjustmentItems:[],stockTransferItems:[],physicalVerificationItems:[],damagedStockItems:[],expiredStockItems:[],nearExpiryItems:[],lowStockItems:[],categories:[],warehouses:[],overstockItems:[],stockLedgerItems:[]}); }
