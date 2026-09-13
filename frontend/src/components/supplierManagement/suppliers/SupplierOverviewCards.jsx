import {
  Landmark,
  ShoppingCart,
  CalendarClock,
  FileText
} from "lucide-react";

const SupplierOverviewCards = ({ supplier }) => {
  const cards = [
    {
      id: "balance",
      title: "Outstanding Balance",
      value: supplier.balance,
      icon: Landmark,
      iconBg: "bg-error-container",
      iconColor: "text-error",
      sublabel: "Total payable to supplier"
    },
    {
      id: "orders",
      title: "Total Orders",
      value: supplier.totalOrders,
      icon: ShoppingCart,
      iconBg: "bg-primary-fixed",
      iconColor: "text-primary",
      sublabel: "All-time purchase orders"
    },
    {
      id: "lastOrder",
      title: "Last Order Date",
      value: supplier.lastOrderDate,
      icon: CalendarClock,
      iconBg: "bg-secondary-container",
      iconColor: "text-secondary",
      sublabel: "Most recent purchase"
    },
    {
      id: "paymentTerms",
      title: "Payment Terms",
      value: supplier.paymentTerms,
      icon: FileText,
      iconBg: "bg-tertiary-fixed",
      iconColor: "text-tertiary",
      sublabel: "Agreed settlement terms"
    }
  ];

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.id}
            className="relative overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest p-5 shadow-sm transition duration-200 hover:shadow-md"
          >
            <div className="mb-4 flex items-start justify-between">
              <div
                className={`flex h-11 w-11 items-center justify-center rounded-xl ${card.iconBg}`}
              >
                <Icon className={`h-5 w-5 ${card.iconColor}`} strokeWidth={2} />
              </div>
            </div>

            <p className="text-xs font-medium uppercase tracking-wider text-outline">
              {card.title}
            </p>
            <p className="mt-1 text-xl font-bold text-on-background">
              {card.value}
            </p>
            <p className="mt-1 text-xs text-on-surface-variant">{card.sublabel}</p>
          </div>
        );
      })}
    </div>
  );
};

export default SupplierOverviewCards;