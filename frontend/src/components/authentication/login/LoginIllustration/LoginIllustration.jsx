import banner from "../../../../assets/medoraxLogin.jpg"

export default function LoginIllustration() {
  return (
    <div 
      className="hidden md:flex flex-col justify-center items-center bg-[#f8f9ff] p-8 relative overflow-hidden h-full"
      style={{
        background: "radial-gradient(circle, rgba(0, 66, 135, 0.06) 0%, rgba(0, 66, 135, 0.01) 100%), #f8f9ff"
      }}
    >
      {/* Animated background circles */}
      <div className="absolute top-0 right-0 w-3/4 h-3/4 bg-gradient-radial from-[#004287]/5 to-transparent animate-pulse-slow pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 w-3/4 h-3/4 bg-gradient-radial from-[#006d40]/5 to-transparent animate-pulse-slow-delayed pointer-events-none"></div>
      
      <div className="relative z-10 w-full max-w-lg transition-all duration-700 hover:scale-105">
        <img
          alt="Medorax Smart Pharmacy Illustration"
          className="w-full h-auto object-contain rounded-lg shadow-sm"
          src={banner}
        />
      </div>

      <style>{`
        @keyframes pulse-slow {
          0%, 100% {
            transform: scale(1);
            opacity: 0.5;
          }
          50% {
            transform: scale(1.2);
            opacity: 1;
          }
        }
        .animate-pulse-slow {
          animation: pulse-slow 8s ease-in-out infinite;
        }
        .animate-pulse-slow-delayed {
          animation: pulse-slow 8s ease-in-out infinite 4s;
        }
        .bg-gradient-radial {
          background-image: radial-gradient(circle, var(--tw-gradient-stops));
        }
      `}</style>
    </div>
  );
}