import "./AuthLayout.css";

import AuthNavbar from "../shared/AuthNavbar";
import AuthBanner from "../shared/AuthBanner";
import AuthFooter from "../shared/AuthFooter";

export default function AuthLayout({ children }) {
  return (
    <div className="auth-layout">

      <AuthNavbar />

      <main className="auth-main">

        <AuthBanner />

        {children}

      </main>

      <AuthFooter />

    </div>
  );
}