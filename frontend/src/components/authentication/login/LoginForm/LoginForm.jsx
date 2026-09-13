// src/components/authentication/login/LoginForm/LoginForm.jsx
import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { loginUser } from "../../../../store/authThunk";
import logo from "../../../../assets/WhatsApp_Image_2026-06-22_at_5.25.21_PM-removebg-preview.png";

export default function LoginForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const result = await dispatch(loginUser({ identifier: email.trim(), password })).unwrap();
      if (result?.user) localStorage.setItem("user", JSON.stringify(result.user));
      const destination = location.state?.from?.pathname || "/";
      navigate(destination, { replace: true });
    } catch (err) {
      const message = err?.detail || err?.message || "Unable to sign in. Check your credentials and license.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md flex flex-col justify-center h-full py-2">
      <div className="flex justify-center">
        <img
          alt="Medorax Logo"
          className="h-24 w-auto object-contain"
          src={logo}
        />
      </div>

      <div className="text-center mb-6">
        <h1 className="text-[32px] leading-[40px] font-semibold tracking-[-0.01em] text-[#121c2a]">
          Welcome Back
        </h1>
        <p className="text-[16px] leading-[24px] font-normal text-[#424751]">
          Access your medical management dashboard
        </p>
      </div>

      <form className="space-y-4" onSubmit={handleSubmit}>
        <div>
          <label
            className="block text-[14px] leading-[20px] font-medium tracking-[0.01em] text-[#424751] mb-1.5"
            htmlFor="email"
          >
            ERP Username, Email or Mobile Number
          </label>
          <input
            id="email"
            type="text"
            className="w-full h-11 px-4 rounded border border-[#c2c6d3] bg-[#ffffff] text-[16px] leading-[24px] font-normal text-[#121c2a] focus:outline-none focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all placeholder:text-[#737782]/50"
            placeholder="ERP username, email or mobile number"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-1.5">
            <label
              className="block text-[14px] leading-[20px] font-medium tracking-[0.01em] text-[#424751]"
              htmlFor="password"
            >
              Password
            </label>
          </div>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              className="w-full h-11 px-4 rounded border border-[#c2c6d3] bg-[#ffffff] text-[16px] leading-[24px] font-normal text-[#121c2a] focus:outline-none focus:border-[#004287] focus:ring-2 focus:ring-[#004287]/20 transition-all placeholder:text-[#737782]/50 pr-12"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="absolute right-4 top-1/2 -translate-y-1/2 text-[#737782] hover:text-[#004287] transition-colors"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              <span className="material-symbols-outlined text-xl">
                {showPassword ? "visibility" : "visibility_off"}
              </span>
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <input
            id="remember"
            type="checkbox"
            className="w-3.5 h-3.5 rounded-sm border-[#c2c6d3] text-[#004287] focus:ring-[#004287]"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          <label
            className="text-[14px] leading-[20px] font-normal text-[#424751] cursor-pointer"
            htmlFor="remember"
          >
            Remember this device for 30 days
          </label>
        </div>

        {error && (
          <p className="text-[14px] leading-[20px] font-normal text-[#ba1a1a] text-center">
            {error}
          </p>
        )}

        <button
          type="submit"
          className="w-full h-11 bg-[#004287] hover:bg-[#1e5aa8] transition-all text-[#ffffff] text-[14px] leading-[20px] font-semibold tracking-[0.01em] rounded shadow-sm flex items-center justify-center gap-2"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="material-symbols-outlined text-[20px] animate-spin">refresh</span>
              Signing In...
            </>
          ) : (
            "Sign In"
          )}
        </button>
      </form>

    </div>
  );
}