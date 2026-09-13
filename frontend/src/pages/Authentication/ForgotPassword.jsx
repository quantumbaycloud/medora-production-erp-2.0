import { useState } from "react";
import api from "../../services/api";
import { Link, useNavigate } from "react-router-dom";
import AuthNavbar from "../../components/authentication/shared/AuthNavbar";
import AuthFooter from "../../components/authentication/shared/AuthFooter";
import logo from "../../assets/WhatsApp_Image_2026-06-22_at_5.25.21_PM-removebg-preview.png"

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/forgot-password", { identifier: email.trim() });
      setIsSubmitted(true);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to start password recovery.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-[#f8f9ff] overflow-hidden">
      <AuthNavbar />
      
      <main className="flex-1 flex flex-col items-center justify-center px-4 overflow-hidden">
        <div className="absolute top-20 left-10 opacity-10 hidden md:block">
          <span className="material-symbols-outlined text-[120px] text-[#004287] select-none">
            add
          </span>
        </div>

        <div className="flex flex-col items-center mb-6">
          <img
            alt="Medorax Logo"
            className="w-20 h-20 mb-3"
            src={logo}
          />
        </div>

        <div className="text-center mb-6 max-w-md">
          <h1 className="text-[32px] leading-[40px] font-semibold tracking-[-0.01em] text-[#121c2a] mb-3">
            Forgot Password?
          </h1>
          <p className="text-[16px] leading-[24px] font-normal text-[#424751] px-4">
            No worries! Enter your email address and we'll send you a link to reset your password.
          </p>
        </div>

        <div className="w-full max-w-[480px] bg-[#ffffff] rounded-lg border border-[#c2c6d3] shadow-sm p-8 mb-4 relative z-10">
          {!isSubmitted ? (
            <form className="space-y-5" onSubmit={handleSubmit}>
              <div>
                <label
                  className="flex items-center gap-2 mb-2.5 text-[#121c2a] text-[14px] leading-[20px] font-semibold tracking-[0.01em]"
                  htmlFor="email"
                >
                  <span className="material-symbols-outlined text-[#004287] text-[20px]">
                    mail
                  </span>
                  Email Address
                </label>
                <div className="relative">
                  <input
                    id="email"
                    type="email"
                    className="w-full h-12 px-4 rounded-lg border border-[#c2c6d3] focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all bg-[#ffffff] text-[16px] leading-[24px] font-normal text-[#121c2a] outline-none placeholder:text-[#737782]/50"
                    placeholder="Enter your email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              {error && <p className="text-sm text-[#ba1a1a] text-center">{error}</p>}
              <button
                type="submit"
                className="w-full h-12 bg-[#004287] hover:bg-[#1e5aa8] transition-all text-[#ffffff] text-[14px] leading-[20px] font-semibold tracking-[0.01em] rounded-lg flex items-center justify-center gap-2 active:scale-95 duration-100"
              >
                <span className="material-symbols-outlined text-[20px]">send</span>
                {loading ? "Sending…" : "Send Reset Link"}
              </button>
            </form>
          ) : (
            <div className="text-center py-6">
              <div className="flex justify-center mb-4">
                <span className="material-symbols-outlined text-[64px] text-[#006d40]">
                  check_circle
                </span>
              </div>
              <h2 className="text-[24px] leading-[32px] font-semibold text-[#121c2a] mb-2">
                Email Sent!
              </h2>
              <p className="text-[16px] leading-[24px] font-normal text-[#424751] mb-4">
                We've sent a password reset link to <strong>{email}</strong>
              </p>
              <button
                onClick={() => {
                  setIsSubmitted(false);
                  setEmail("");
                }}
                className="text-[#004287] hover:underline font-semibold"
              >
                Try another email
              </button>
            </div>
          )}
        </div>

        <div className="text-center">
          <p className="text-[14px] leading-[20px] font-normal text-[#424751]">
            Remember your password?{" "}
            <Link
              to="/login"
              className="text-[#004287] font-semibold hover:underline transition-all"
            >
              Back to Login
            </Link>
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-[1440px] px-4 mt-6">
          <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-[#eff4ff]/50 transition-colors">
            <div className="bg-[#004287]/10 p-2.5 rounded-full flex items-center justify-center">
              <span className="material-symbols-outlined text-[#004287] text-[20px]">
                verified_user
              </span>
            </div>
            <div>
              <h3 className="text-[14px] leading-[20px] font-semibold tracking-[0.01em] text-[#121c2a]">
                Secure & Trusted
              </h3>
              <p className="text-[12px] leading-[16px] font-normal text-[#424751]">
                Your data is safe with us
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-[#eff4ff]/50 transition-colors">
            <div className="bg-[#004287]/10 p-2.5 rounded-full flex items-center justify-center">
              <span className="material-symbols-outlined text-[#004287] text-[20px]">
                lock_reset
              </span>
            </div>
            <div>
              <h3 className="text-[14px] leading-[20px] font-semibold tracking-[0.01em] text-[#121c2a]">
                Easy Recovery
              </h3>
              <p className="text-[12px] leading-[16px] font-normal text-[#424751]">
                Reset your password in a few simple steps
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-[#eff4ff]/50 transition-colors">
            <div className="bg-[#004287]/10 p-2.5 rounded-full flex items-center justify-center">
              <span className="material-symbols-outlined text-[#004287] text-[20px]">
                headset_mic
              </span>
            </div>
            <div>
              <h3 className="text-[14px] leading-[20px] font-semibold tracking-[0.01em] text-[#121c2a]">
                24/7 Support
              </h3>
              <p className="text-[12px] leading-[16px] font-normal text-[#424751]">
                We're here to help you anytime
              </p>
            </div>
          </div>
        </div>
      </main>

      <AuthFooter />
    </div>
  );
}