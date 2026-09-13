import { useState } from "react";
import { Search, Download, RefreshCw } from "lucide-react";
import { TABS } from "../../data/reports/data";
import { currentStockItems } from "../../data/inventoryManagement/inventoryData";
import { SalesStats, SalesTable } from "../../components/reports/SalesTab";
import { PurchaseStats, PurchaseTable } from "../../components/reports/PurchaseTab";
import { InventoryStats, InventoryTable } from "../../components/reports/InventoryTab";
import { GSTStats, GSTTable } from "../../components/reports/GSTTab";
import { ProfitStats, ProfitTable } from "../../components/reports/ProfitTab";
import { CustomerStats, CustomerTable } from "../../components/reports/CustomerTab";
import { SupplierStats, SupplierTable } from "../../components/reports/SupplierTab";

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState("sales");
  const [period, setPeriod] = useState("Monthly");
  const [branch, setBranch] = useState("All Branches");
  const [status, setStatus] = useState("All Status");
  const [supplier, setSupplier] = useState("All Suppliers");
  const [inventorySubtype, setInventorySubtype] = useState("Stock Movement");
  const [gstFromDate, setGstFromDate] = useState("2023-10-01");
  const [gstToDate, setGstToDate] = useState("2023-10-28");
  const [customerType, setCustomerType] = useState("All Customers");
  const [profitProduct, setProfitProduct] = useState("All Products");
  const [supplierFilter, setSupplierFilter] = useState("All Suppliers");
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");

  const changeTab = (tab) => {
    setActiveTab(tab);
    setPage(1);
    if (tab === "purchase") {
      setStatus("All Status");
      setSupplier("All Suppliers");
      setPeriod("Monthly");
    }
    if (tab === "customer") setCustomerType("All Customers");
    if (tab === "inventory") setInventorySubtype("Stock Movement");
    if (tab === "supplier") setSupplierFilter("All Suppliers");
  };

  // Render filters based on active tab
  const renderFilters = () => {
    const commonFilterClass = "px-3 py-2 border border-[#c2c6d3] rounded focus:ring-2 focus:ring-[#d6e3ff] focus:border-[#004287] outline-none bg-white text-[#121c2a] text-sm";

    switch (activeTab) {
      case "sales":
        return (
          <>
            <select
              value={period}
              onChange={(e) => {
                setPeriod(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-32`}
            >
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
              <option value="Yearly">Yearly</option>
            </select>
            <select
              value={branch}
              onChange={(e) => {
                setBranch(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-40`}
            >
              <option value="All Branches">All Branches</option>
              <option value="Branch 1">Branch 1</option>
              <option value="Branch 2">Branch 2</option>
            </select>
          </>
        );
      case "purchase":
        return (
          <>
            <select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-36`}
            >
              <option value="All Status">All Status</option>
              <option value="Delivered">Delivered</option>
              <option value="Pending">Pending</option>
              <option value="Shipped">Shipped</option>
            </select>
            <select
              value={supplier}
              onChange={(e) => {
                setSupplier(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-40`}
            >
              <option value="All Suppliers">All Suppliers</option>
              {supplierData.map((item) => (
                <option key={item.id} value={item.name}>{item.name}</option>
              ))}
            </select>
          </>
        );
      case "inventory":
        return (
          <div className="flex border border-[#c2c6d3] rounded overflow-hidden">
            <button
              onClick={() => {
                setInventorySubtype("Stock Movement");
                setPage(1);
              }}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                inventorySubtype === "Stock Movement"
                  ? "bg-[#004287] text-white"
                  : "bg-white text-[#121c2a] hover:bg-[#eff4ff]"
              }`}
            >
              Stock Movement
            </button>
            <button
              onClick={() => {
                setInventorySubtype("Expiry Reports");
                setPage(1);
              }}
              className={`px-4 py-2 text-sm font-medium transition-colors border-l border-[#c2c6d3] ${
                inventorySubtype === "Expiry Reports"
                  ? "bg-[#004287] text-white"
                  : "bg-white text-[#121c2a] hover:bg-[#eff4ff]"
              }`}
            >
              Expiry Reports
            </button>
          </div>
        );
      case "gst":
        return (
          <div className="flex items-center gap-2">
            <input
              type="date"
              value={gstFromDate}
              onChange={(e) => {
                setGstFromDate(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-36`}
            />
            <span className="text-[#424751] text-sm">to</span>
            <input
              type="date"
              value={gstToDate}
              onChange={(e) => {
                setGstToDate(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-36`}
            />
          </div>
        );
      case "profit":
        return (
          <>
            <select
              value={period}
              onChange={(e) => {
                setPeriod(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-32`}
            >
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
              <option value="Yearly">Yearly</option>
            </select>
            <select
              value={profitProduct}
              onChange={(e) => {
                setProfitProduct(e.target.value);
                setPage(1);
              }}
              className={`${commonFilterClass} w-full md:w-44`}
            >
              <option value="All Products">All Products</option>
              {[...new Set(currentStockItems.map((item) => item.name).filter(Boolean))].map((name) => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>
          </>
        );
      case "customer":
        return (
          <select
            value={customerType}
            onChange={(e) => {
              setCustomerType(e.target.value);
              setPage(1);
            }}
            className={`${commonFilterClass} w-full md:w-44`}
          >
            <option value="All Customers">All Customers</option>
            <option value="Repeat">Repeat</option>
            <option value="One-Time">One-Time</option>
          </select>
        );
      case "supplier":
        return (
          <select
            value={supplierFilter}
            onChange={(e) => {
              setSupplierFilter(e.target.value);
              setPage(1);
            }}
            className={`${commonFilterClass} w-full md:w-44`}
          >
            <option value="All Suppliers">All Suppliers</option>
            <option value="Has Outstanding">Has Outstanding</option>
            <option value="Fully Paid">Fully Paid</option>
          </select>
        );
      default:
        return null;
    }
  };

  // Render stats based on active tab
  const renderStats = () => {
    switch (activeTab) {
      case "sales":
        return <SalesStats period={period} />;
      case "purchase":
        return <PurchaseStats />;
      case "inventory":
        return <InventoryStats />;
      case "gst":
        return <GSTStats />;
      case "profit":
        return <ProfitStats period={period} />;
      case "customer":
        return <CustomerStats />;
      case "supplier":
        return <SupplierStats />;
      default:
        return null;
    }
  };

  // Render table based on active tab
  const renderTable = () => {
    switch (activeTab) {
      case "sales":
        return <SalesTable period={period} branch={branch} page={page} setPage={setPage} search={search} />;
      case "purchase":
        return <PurchaseTable status={status} supplier={supplier} page={page} setPage={setPage} search={search} />;
      case "inventory":
        return <InventoryTable inventorySubtype={inventorySubtype} page={page} setPage={setPage} search={search} />;
      case "gst":
        return <GSTTable gstFromDate={gstFromDate} gstToDate={gstToDate} page={page} setPage={setPage} search={search} />;
      case "profit":
        return <ProfitTable period={period} profitProduct={profitProduct} page={page} setPage={setPage} search={search} />;
      case "customer":
        return <CustomerTable customerType={customerType} page={page} setPage={setPage} search={search} />;
      case "supplier":
        return <SupplierTable supplierFilter={supplierFilter} page={page} setPage={setPage} search={search} />;
      default:
        return null;
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#f8f9ff]">
      <main className="flex-1 overflow-y-auto p-6 space-y-6 pt-0">
        {/* Tab Navigation */}
        <div className="bg-white border-b border-[#c2c6d3] sticky top-0 z-20 mt-4">
          <div className="flex overflow-x-auto no-scrollbar gap-8 py-2 whitespace-nowrap px-6">
            <div className="flex flex-col gap-2">
              <span className="text-[12px] font-bold text-[#004287] uppercase tracking-wider opacity-60 px-1">
                Reports
              </span>
              <div className="flex gap-4 overflow-y-hidden pb-2">
                {TABS.map((t) => (
                  <a
                    key={t.key}
                    onClick={() => changeTab(t.key)}
                    className={`text-[16px] text-[#004287] relative px-1 cursor-pointer transition-opacity ${
                      activeTab === t.key ? "font-bold opacity-100" : "opacity-80 hover:opacity-100"
                    }`}
                  >
                    {t.label}
                    <div
                      className={`absolute -bottom-[10px] left-0 right-0 h-1 rounded-t-full ${
                        activeTab === t.key ? "bg-[#004287]" : "hidden"
                      }`}
                    ></div>
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="md:hidden font-bold text-2xl tracking-tight text-[#121c2a] mb-4">Reports</div>

        {/* 1. Stats Cards */}
        {renderStats()}

        {/* 2. Search Box with Filters, Refresh & Export */}
        <div className="bg-white rounded border border-[#c2c6d3] p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative flex-1 w-full md:w-auto min-w-[200px]">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#424751] pointer-events-none" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search records..."
              className="w-full h-9 pl-9 pr-3 rounded border border-[#c2c6d3] bg-white text-sm text-[#121c2a] placeholder:text-[#424751] outline-none transition-colors focus:border-[#004287] focus:ring-2 focus:ring-[#d6e3ff]"
            />
          </div>

          <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
            {renderFilters()}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setPage(1)}
              className="p-2 border border-[#c2c6d3] rounded hover:bg-[#eff4ff] transition-colors flex items-center justify-center text-[#424751]"
              title="Refresh"
            >
              <RefreshCw size={18} />
            </button>
            <button
              onClick={() => alert("Export CSV")}
              className="flex items-center gap-2 px-4 py-2 bg-[#004287] text-white font-bold rounded transition-colors hover:bg-[#235eac]"
            >
              <Download size={18} />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* 3. Table */}
        {renderTable()}
      </main>
    </div>
  );
}