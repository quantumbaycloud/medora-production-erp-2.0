import { LogIn, LogOut } from "lucide-react";

const ActionButtons = ({ onCheckIn, onCheckOut, disabled }) => {
  return (
    <div className="grid grid-cols-2 gap-4">
      <button
        type="button"
        onClick={onCheckIn}
        disabled={disabled}
        className="flex flex-col items-center justify-center gap-2 rounded-xl bg-primary py-6 text-on-primary shadow-md transition-all hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <LogIn size={32} strokeWidth={2.2} fill="currentColor" />
        <span className="text-2xl font-bold">Check In</span>
      </button>
      <button
        type="button"
        onClick={onCheckOut}
        disabled={disabled}
        className="flex flex-col items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 py-6 text-on-primary shadow-md transition-all hover:brightness-110 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <LogOut size={32} strokeWidth={2.2} fill="currentColor" />
        <span className="text-2xl font-bold">Check Out</span>
      </button>
    </div>
  );
};

export default ActionButtons;