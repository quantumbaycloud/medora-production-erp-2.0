import { useState } from "react";
import { Outlet } from "react-router-dom";

import AppSidebar from "../../components/navigation/AppSidebar";
import AppTopbar from "../../components/navigation/AppTopbar";
import ERPDataBootstrap from "../../components/system/ERPDataBootstrap";

export default function DashboardLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <AppSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <div className="min-h-screen md:ml-[260px]">
        <AppTopbar onMenuClick={() => setIsSidebarOpen(true)} />
        <main className="min-h-screen px-4 pb-8 pt-20 md:px-8 md:pt-24">
          <ERPDataBootstrap>
            <Outlet />
          </ERPDataBootstrap>
        </main>
      </div>
    </div>
  );
}
