import api from "../services/api";

export const getDeviceIdentifier = () => {
  const key = "medorax.erp.device_id";
  let value = localStorage.getItem(key);
  if (!value) {
    value = crypto.randomUUID();
    localStorage.setItem(key, value);
  }
  return value;
};

const isElectron = () => Boolean(window.medoraxDesktop?.isDesktop);
const platform = () => isElectron() ? "windows" : "web";

const authService = {
  async login(data) {
    const response = await api.post("/auth/login", {
      identifier: String(data.identifier || "").trim(),
      password: data.password,
      device_identifier: data.device_identifier || getDeviceIdentifier(),
      platform: platform(),
      device_name: isElectron()
        ? `MEDORAX ERP Windows Desktop (${navigator.userAgent.slice(0, 120)})`
        : navigator.userAgent.slice(0, 255),
      app_version: isElectron() ? "2.0.0" : undefined,
    });
    const result = response.data || {};
    if (result.access_token) localStorage.setItem("accessToken", result.access_token);
    if (result.refresh_token) localStorage.setItem("refreshToken", result.refresh_token);
    if (result.device_identifier) localStorage.setItem("medorax.erp.device_id", result.device_identifier);
    if (result.user) localStorage.setItem("user", JSON.stringify(result.user));
    return response;
  },
  async refresh() {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) throw new Error("No refresh token");
    return api.post("/auth/refresh", { refresh_token: refreshToken });
  },
  async logout() {
    try { return await api.post("/auth/logout"); }
    finally { clearAuth(); }
  },
};

function clearAuth() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("user");
}

export default authService;
