export const TABS = [
  { key: "sales", label: "Sales" },
  { key: "purchase", label: "Purchase" },
  { key: "inventory", label: "Inventory" },
  { key: "gst", label: "GST" },
  { key: "profit", label: "Profit" },
  { key: "customer", label: "Customer" },
  { key: "supplier", label: "Supplier" },
];

export const STAT_LABELS = {
  sales: ["Total Sales", "Total Revenue", "Total Transactions"],
  purchase: ["Total Purchases", "Total Amount", "Pending Orders"],
  inventory: ["Total Items", "Expiring Items", "Total SKUs"],
  gst: ["Taxable Value", "GST Collected", "Total Invoices"],
  profit: ["Total Profit", "Avg. Margin %", "Best Performing Product"],
  customer: ["Total Customers", "Total Revenue", "Repeat Rate"],
  supplier: ["Total Suppliers", "Total Outstanding", "On-Time Delivery Rate"],
};

export const ROWS_PER_PAGE = 5;

export { 
  salesData,
  profitData,
  purchaseData,
  inventoryData,
  gstData,
  customerData,
  supplierData
} from "./mockData";