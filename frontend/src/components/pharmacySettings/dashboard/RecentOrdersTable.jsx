import { MoreVertical } from "lucide-react";
import StatusChip from "../common/StatusChip";
import { recentOrders } from "../../../data/pharmacySettings/pharmacySettingsData";

const statusTone = {
  Paid: "success",
  Pending: "info",
  Cancelled: "error",
};

const RecentOrdersTable = () => {
  return (
    <section className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="flex items-center justify-between border-b border-outline-variant px-5 py-4 md:px-6">
        <div>
          <h4 className="text-lg font-bold text-on-background">Recent orders</h4>
          <p className="mt-1 text-xs text-on-surface-variant">Latest transactions across branches</p>
        </div>
        <button
          type="button"
          className="text-sm font-bold text-primary transition-colors hover:underline"
        >
          View All
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="cp-table-header">
            <tr>
              <th className="px-6 py-3">Order ID</th>
              <th className="px-6 py-3">Customer</th>
              <th className="px-6 py-3">Branch</th>
              <th className="px-6 py-3">Amount</th>
              <th className="px-6 py-3">Status</th>
              <th className="px-6 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {recentOrders.map((order) => (
              <tr key={order.orderId} className="cp-table-row-hover">
                <td className="px-6 py-4 font-semibold text-on-background">
                  {order.orderId}
                </td>
                <td className="px-6 py-4 text-on-surface-variant">{order.customer}</td>
                <td className="px-6 py-4 text-on-surface-variant">{order.branch}</td>
                <td className="px-6 py-4 font-bold text-on-background">{order.amount}</td>
                <td className="px-6 py-4">
                  <StatusChip tone={statusTone[order.status]}>{order.status}</StatusChip>
                </td>
                <td className="px-6 py-4 text-right">
                  <button
                    type="button"
                    aria-label={`Actions for order ${order.orderId}`}
                    className="rounded-full p-1.5 text-on-surface-variant transition-colors hover:bg-surface-container-low hover:text-primary"
                  >
                    <MoreVertical size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default RecentOrdersTable;
