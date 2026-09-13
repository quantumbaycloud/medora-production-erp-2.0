import {
  Banknote,
  CreditCard,
  QrCode,
  ArrowRight,
} from "lucide-react";

const paymentMethods = [
  { id: "cash", label: "Cash", icon: Banknote },
  { id: "card", label: "Card", icon: CreditCard },
  { id: "upi", label: "UPI", icon: QrCode },
];

const CartSummary = ({ subtotal, tax, discount, total, onPay }) => {
  return (
    <div className="overflow-hidden rounded-xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="border-b border-outline-variant p-6">
        <h3 className="text-lg font-semibold text-on-background">Billing Summary</h3>
      </div>

      <div className="space-y-4 p-6">
        <div className="flex justify-between text-sm text-on-surface-variant">
          <span>Subtotal</span>
          <span className="font-semibold text-on-background">
            ${subtotal.toFixed(2)}
          </span>
        </div>
        <div className="flex justify-between text-sm text-on-surface-variant">
          <span>Discount</span>
          <span className="font-semibold text-secondary">
            -${discount.toFixed(2)}
          </span>
        </div>
        <div className="flex justify-between text-sm text-on-surface-variant">
          <span>Tax (GST)</span>
          <span className="font-semibold text-on-background">${tax.toFixed(2)}</span>
        </div>

        <div className="flex items-center justify-between border-t border-outline-variant pt-4">
          <span className="text-base font-semibold text-on-background">
            Grand Total
          </span>
          <span className="text-2xl font-bold text-primary">
            ${total.toFixed(2)}
          </span>
        </div>
      </div>

      <div className="px-6">
        <p className="mb-3 text-xs font-bold uppercase tracking-wider text-outline">
          Payment Method
        </p>
        <div className="grid grid-cols-3 gap-2 rounded-lg bg-surface-container p-1">
          {paymentMethods.map((method) => {
            const Icon = method.icon;
            return (
              <button
                key={method.id}
                type="button"
                className="flex flex-col items-center gap-1 rounded-md px-2 py-3 text-xs font-semibold text-on-surface-variant transition hover:bg-surface-container-lowest hover:text-primary hover:shadow-sm"
              >
                <Icon size={18} />
                {method.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-6">
        <button
          type="button"
          onClick={onPay}
          className="flex w-full items-center justify-center gap-3 rounded-xl bg-primary py-4 text-base font-bold text-on-primary shadow-lg transition-transform duration-200 hover:scale-[1.02] active:scale-95"
        >
          <span>Pay Now</span>
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  );
};

export default CartSummary;