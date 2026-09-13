
export default function AuthFooter() {
  return (
    <footer className="bg-[#f8f9ff] border-t border-[#c2c6d3] flex-shrink-0">
      <div className="w-full py-3 px-2 flex flex-col md:flex-row justify-between items-center gap-2 max-w-[1440px] mx-auto">
        <span className="text-[14px] leading-[20px] font-semibold tracking-[0.01em] text-[#004287]">
          Medorax
        </span>
        
        <div className="flex flex-wrap justify-center gap-x-6 gap-y-1">
          <a
            className="text-[12px] leading-[16px] font-semibold text-[#424751] hover:text-[#004287] transition-colors duration-200"
            href="#"
          >
            Privacy Policy
          </a>
          <a
            className="text-[12px] leading-[16px] font-semibold text-[#424751] hover:text-[#004287] transition-colors duration-200"
            href="#"
          >
            Terms of Service
          </a>
          <a
            className="text-[12px] leading-[16px] font-semibold text-[#424751] hover:text-[#004287] transition-colors duration-200"
            href="#"
          >
            Security
          </a>
          <a
            className="text-[12px] leading-[16px] font-semibold text-[#424751] hover:text-[#004287] transition-colors duration-200"
            href="#"
          >
            Help Center
          </a>
        </div>
        
        <p className="text-[12px] leading-[16px] font-normal text-[#424751]">
          © 2024 Medorax. All rights reserved.
        </p>
      </div>
    </footer>
  );
}