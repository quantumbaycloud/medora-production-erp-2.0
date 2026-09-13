// src/pages/Authentication/Login.jsx
import LoginForm from "../../components/authentication/login/LoginForm/LoginForm";
import AuthNavbar from "../../components/authentication/shared/AuthNavbar";
import AuthFooter from "../../components/authentication/shared/AuthFooter";
import LoginIllustration from "../../components/authentication/login/LoginIllustration/LoginIllustration";

export default function Login() {
  return (
    <div className="h-screen flex flex-col bg-[#f8f9ff] overflow-hidden">
      <AuthNavbar />
      
      <main className="flex-1 flex items-stretch overflow-hidden">
        <div className="max-w-[1440px] mx-auto w-full grid grid-cols-1 md:grid-cols-2 overflow-hidden">
          <LoginIllustration />
          
          <div className="flex flex-col justify-center items-center px-4 md:px-8 py-6 bg-[#ffffff] overflow-hidden">
            <LoginForm />
          </div>
        </div>
      </main>

      <AuthFooter />
    </div>
  );
}