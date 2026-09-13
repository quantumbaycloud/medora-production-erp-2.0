import api, { withPharmacy } from "./api";

export async function createInvoice({ cartItems, paymentMethod = "Cash", customerId = null, customerName = null, branchId = null }) {
  const items = cartItems.map((item) => ({
    medicine_id: item.medicine_id || item.id,
    batch_number: item.batch_number || item.batch || "",
    quantity: Number(item.quantity),
    discount_type: "flat",
    discount_value: 0,
  }));
  if (items.some((item) => !item.batch_number)) throw new Error("Every billed medicine must have a valid batch selected.");
  const { data } = await api.post("/billing/invoice", { customer_id: customerId, customer_name: customerName, branch_id: branchId, items, payment_method: paymentMethod, is_credit: false }, { params: withPharmacy() });
  return data;
}
