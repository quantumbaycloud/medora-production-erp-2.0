import { categories, warehouses } from "../../../data/inventoryManagement/inventoryData";

export const addStockFields = [
  { name: "itemName", label: "Item Name", type: "text", placeholder: "Search or enter item name...", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Item Code", type: "text", placeholder: "e.g. MED-AMX-050", required: true },
  { name: "category", label: "Category", type: "select", options: categories, required: true },
  { name: "quantity", label: "Quantity", type: "number", min: "0", placeholder: "0", required: true },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "warehouse", label: "Warehouse / Location", type: "select", options: warehouses, required: true, fullWidth: true },
  { name: "batchNumber", label: "Batch Number", type: "text", placeholder: "e.g. B-2024-001" },
  { name: "mfgDate", label: "Mfg Date", type: "date" },
  { name: "expiryDate", label: "Expiry Date", type: "date", fullWidth: true },
];

export const openingStockFields = [
  { name: "itemName", label: "Item Name", type: "text", placeholder: "Search or enter item name...", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Item Code", type: "text", placeholder: "e.g. MED-AMX-050", required: true },
  { name: "category", label: "Category", type: "select", options: categories, required: true },
  { name: "openingQty", label: "Opening Quantity", type: "number", min: "0", placeholder: "0", required: true },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "warehouse", label: "Warehouse / Location", type: "select", options: warehouses, required: true },
  { name: "periodStartDate", label: "Period Start Date", type: "date", required: true },
  { name: "remarks", label: "Remarks / Notes", type: "textarea", placeholder: "Add any relevant details...", fullWidth: true },
];

export const closingStockFields = [
  { name: "itemName", label: "Item Name", type: "text", placeholder: "Search or enter item name...", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Item Code", type: "text", placeholder: "e.g. MED-AMX-050", required: true },
  { name: "category", label: "Category", type: "select", options: categories, required: true },
  { name: "closingQty", label: "Closing Quantity", type: "number", min: "0", placeholder: "0", required: true },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "warehouse", label: "Warehouse / Location", type: "select", options: warehouses, required: true },
  { name: "periodEndDate", label: "Period End Date", type: "date", required: true },
  { name: "remarks", label: "Remarks / Notes", type: "textarea", placeholder: "Add any relevant details...", fullWidth: true },
];

export const availableStockFields = [
  { name: "itemName", label: "Item Name", type: "text", placeholder: "Search or enter item name...", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Item Code", type: "text", placeholder: "e.g. MED-AMX-050", required: true },
  { name: "category", label: "Category", type: "select", options: categories, required: true },
  { name: "totalQty", label: "Total Stock Quantity", type: "number", min: "0", placeholder: "0", required: true },
  { name: "reservedQty", label: "Reserved Quantity", type: "number", min: "0", placeholder: "0" },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "warehouse", label: "Warehouse / Location", type: "select", options: warehouses, required: true },
];

export const reservedStockFields = [
  { name: "itemName", label: "Item Name", type: "text", placeholder: "Search or enter item name...", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Item Code", type: "text", placeholder: "e.g. MED-AMX-050", required: true },
  { name: "category", label: "Category", type: "select", options: categories, required: true },
  { name: "reservedQty", label: "Reserved Quantity", type: "number", min: "1", placeholder: "0", required: true },
  { name: "reservedFor", label: "Reserved For", type: "text", placeholder: "e.g. St. Jude Hospital", required: true },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "warehouse", label: "Warehouse / Location", type: "select", options: warehouses, required: true },
  { name: "reservationDate", label: "Reservation Date", type: "date", required: true },
];

export const addBatchFields = [
  { name: "batchNumber", label: "Batch Number", type: "text", placeholder: "e.g. B-2401-AX", required: true },
  { name: "itemName", label: "Item Name", type: "text", placeholder: "e.g. Amoxicillin 500mg", required: true, fullWidth: true },
  { name: "sku", label: "SKU / Code", type: "text", placeholder: "e.g. SKU-AMX-500", required: true },
  { name: "mfgDate", label: "Mfg Date", type: "date", required: true },
  { name: "expiryDate", label: "Expiry Date", type: "date", required: true },
  { name: "quantity", label: "Quantity", type: "number", min: "0", placeholder: "0", required: true },
  { name: "unit", label: "Unit", type: "select", options: ["Tablets", "Strips", "Bottles", "Vials", "Boxes"], required: true },
  { name: "location", label: "Location", type: "select", options: warehouses, required: true },
];

