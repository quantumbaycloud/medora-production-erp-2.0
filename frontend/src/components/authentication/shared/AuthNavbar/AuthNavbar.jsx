// src/components/authentication/shared/AuthNavbar.jsx
import logo from "../../../../assets/WhatsApp_Image_2026-06-22_at_5.25.21_PM-removebg-preview.png";

export default function AuthNavbar() {
  return (
    <header className="bg-[#f8f9ff] border-b border-[#c2c6d3] flex-shrink-0">
      <nav className="flex justify-between items-center w-full max-w-full px-4 md:px-6 h-14">
        <div className="flex items-center ">
          <img
            alt="Medorax Logo"
            className="h-14 w-auto object-contain"
            src={logo}
          />
          <span className="text-[24px] leading-[32px] font-semibold text-[#004287]">
            Medorax
          </span>
        </div>
        
        <div className="flex items-center gap-4">
          <button
            className="hidden md:flex items-center gap-2 text-[14px] leading-[20px] font-medium tracking-[0.01em] text-[#424751] hover:bg-[#eff4ff] rounded-full px-4 py-2 transition-colors cursor-pointer"
            onClick={() => console.log("Help clicked")}
          >
            <span className="material-symbols-outlined text-[20px]">
              help
            </span>
            Help
          </button>
        </div>
      </nav>
    </header>
  );
}