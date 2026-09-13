// src/pages/Authentication/ChangePassword.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthNavbar from "../../components/authentication/shared/AuthNavbar";
import AuthFooter from "../../components/authentication/shared/AuthFooter";
import logo from "../../assets/WhatsApp_Image_2026-06-22_at_5.25.21_PM-removebg-preview.png";
import banner from "../../assets/changePassImg.jpg";

export default function ChangePassword() {
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // Password requirements
  const requirements = [
    { id: "length", label: "At least 8 characters", met: newPassword.length >= 8 },
    { id: "uppercase", label: "One uppercase letter", met: /[A-Z]/.test(newPassword) },
    { id: "number", label: "One numerical digit", met: /\d/.test(newPassword) },
    { id: "special", label: "One special character (@#$%^&*)", met: /[@#$%^&*]/.test(newPassword) },
  ];

  const allRequirementsMet = requirements.every(req => req.met);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (currentPassword.length < 1) {
      setError("Please enter your current password");
      return;
    }

    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (!allRequirementsMet) {
      setError("Please meet all password requirements");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      setSuccess(true);
      
      setTimeout(() => {
        navigate("/login", { 
          state: { 
            message: "Password changed successfully! Please login with your new password." 
          } 
        });
      }, 2000);
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8f9ff]">
      <AuthNavbar />
      
      <main className="flex-1 flex flex-col lg:flex-row overflow-y-auto">
        {/* Left Side: Hero Illustration */}
        <div className="hidden lg:flex lg:w-1/2 bg-[#eff4ff] items-center justify-center px-6 py-8 relative overflow-hidden min-h-[500px]">
          <div className="absolute inset-0 opacity-10">
            <div 
              className="absolute inset-0" 
              style={{ 
                backgroundImage: "radial-gradient(#004287 1px, transparent 1px)", 
                backgroundSize: "40px 40px" 
              }}
            ></div>
          </div>
          <div className="absolute -bottom-20 -left-20 w-64 h-64 bg-[#004287]/5 rounded-full blur-3xl"></div>
          <div className="absolute -top-20 -right-20 w-80 h-80 bg-[#006d40]/5 rounded-full blur-3xl"></div>
          
          <div className="relative z-10 max-w-md text-center">
            <div className="mb-3 rounded-xl shadow-sm p-2 bg-white">
              <img
                alt="Security Illustration"
                className="w-full h-auto object-cover rounded-lg"
                src={banner}
              />
            </div>
            <h1 className="text-[28px] leading-[36px] font-bold tracking-[-0.01em] bg-gradient-to-r from-[#004287] via-[#006d40] to-[#004287] bg-clip-text text-transparent mb-2">
              Secure Your Account
            </h1>
            <p className="text-[14px] leading-[20px] font-normal text-[#424751]">
              Maintaining strict data privacy is our top priority. Update your credentials regularly to ensure the safety of your clinical and medical delivery records.
            </p>
          </div>
        </div>

        {/* Right Side: Form Area */}
        <div className="w-full lg:w-1/2 flex items-center justify-center px-4 md:px-8 py-8 bg-[#ffffff]">
          <div className="w-full max-w-md">
            {/* Logo */}
            <div className="flex justify-center mb-3">
              <img
                alt="Medorax Logo"
                className="h-20 w-auto object-contain"
                src={logo}
              />
            </div>

            {/* Header */}
            <div className="mb-4">
              <h2 className="text-[20px] leading-[28px] font-semibold text-[#121c2a] mb-1">
                Change Password
              </h2>
              <p className="text-[13px] leading-[18px] font-normal text-[#424751]">
                Please enter your current password and choose a new secure password.
              </p>
            </div>

            {/* Success Message */}
            {success && (
              <div className="mb-3 p-3 bg-[#006d40]/10 border border-[#006d40] rounded-lg text-[#006d40] text-[13px] leading-[18px] flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px]">check_circle</span>
                Password changed successfully! Redirecting...
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mb-3 p-3 bg-[#ba1a1a]/10 border border-[#ba1a1a] rounded-lg text-[#ba1a1a] text-[13px] leading-[18px] flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px]">error</span>
                {error}
              </div>
            )}

            <form className="space-y-3" onSubmit={handleSubmit}>
              {/* Current Password */}
              <div>
                <label
                  className="block text-[11px] leading-[16px] font-medium tracking-[0.02em] text-[#424751] mb-1 ml-1"
                  htmlFor="current-password"
                >
                  Current Password
                </label>
                <div className="relative">
                  <input
                    id="current-password"
                    type={showCurrentPassword ? "text" : "password"}
                    className="w-full h-10 px-3 rounded-lg border border-[#c2c6d3] focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all bg-[#ffffff] text-[14px] leading-[20px] font-normal text-[#121c2a] outline-none placeholder:text-[#737782]/50 pr-10"
                    placeholder="••••••••"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#737782] hover:text-[#004287] transition-colors"
                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                  >
                    <span className="material-symbols-outlined text-[18px]">
                      {showCurrentPassword ? "visibility_off" : "visibility"}
                    </span>
                  </button>
                </div>
              </div>

              {/* New Password */}
              <div>
                <label
                  className="block text-[11px] leading-[16px] font-medium tracking-[0.02em] text-[#424751] mb-1 ml-1"
                  htmlFor="new-password"
                >
                  New Password
                </label>
                <div className="relative">
                  <input
                    id="new-password"
                    type={showNewPassword ? "text" : "password"}
                    className="w-full h-10 px-3 rounded-lg border border-[#c2c6d3] focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all bg-[#ffffff] text-[14px] leading-[20px] font-normal text-[#121c2a] outline-none placeholder:text-[#737782]/50 pr-10"
                    placeholder="••••••••"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#737782] hover:text-[#004287] transition-colors"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                  >
                    <span className="material-symbols-outlined text-[18px]">
                      {showNewPassword ? "visibility_off" : "visibility"}
                    </span>
                  </button>
                </div>
              </div>

              {/* Confirm Password */}
              <div>
                <label
                  className="block text-[11px] leading-[16px] font-medium tracking-[0.02em] text-[#424751] mb-1 ml-1"
                  htmlFor="confirm-password"
                >
                  Confirm New Password
                </label>
                <div className="relative">
                  <input
                    id="confirm-password"
                    type={showConfirmPassword ? "text" : "password"}
                    className="w-full h-10 px-3 rounded-lg border border-[#c2c6d3] focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all bg-[#ffffff] text-[14px] leading-[20px] font-normal text-[#121c2a] outline-none placeholder:text-[#737782]/50 pr-10"
                    placeholder="••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#737782] hover:text-[#004287] transition-colors"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    <span className="material-symbols-outlined text-[18px]">
                      {showConfirmPassword ? "visibility_off" : "visibility"}
                    </span>
                  </button>
                </div>
              </div>

              {/* Password Requirements */}
              <div className="py-1.5 px-1 space-y-1.5">
                <h3 className="text-[10px] leading-[14px] font-medium tracking-[0.03em] uppercase text-[#737782]">
                  Security Requirements
                </h3>
                <ul className="space-y-1">
                  {requirements.map((req) => (
                    <li key={req.id} className="flex items-center gap-1.5 text-[12px] leading-[16px] font-normal text-[#424751]">
                      <span className={`material-symbols-outlined text-[16px] ${req.met ? 'text-[#006d40]' : 'text-[#c2c6d3]'}`}>
                        {req.met ? "check_circle" : "radio_button_unchecked"}
                      </span>
                      {req.label}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Action Buttons */}
              <div className="pt-1 flex flex-col gap-2">
                <button
                  type="submit"
                  className="w-full h-10 bg-[#004287] hover:bg-[#1e5aa8] transition-all text-[#ffffff] text-[13px] leading-[18px] font-semibold tracking-[0.01em] rounded-lg flex items-center justify-center gap-2 active:scale-[0.98] shadow-sm"
                  disabled={isLoading || success}
                >
                  {isLoading ? (
                    <>
                      <span className="material-symbols-outlined text-[18px] animate-spin">refresh</span>
                      Processing...
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[18px]">lock</span>
                      Update Password
                    </>
                  )}
                </button>

                <Link
                  to="/"
                  className="w-full h-10 flex items-center justify-center text-[13px] leading-[18px] font-semibold tracking-[0.01em] text-[#424751] hover:text-[#004287] transition-colors rounded-lg"
                >
                  Back to Security Settings
                </Link>
              </div>
            </form>

            {/* Footer */}
            <div className="mt-4 text-center">
              <p className="text-[11px] leading-[16px] font-normal text-[#424751]/60">
                © 2024 Medorax Health Systems. Secure Data Portal.
              </p>
            </div>
          </div>
        </div>
      </main>

      <AuthFooter />
    </div>
  );
}