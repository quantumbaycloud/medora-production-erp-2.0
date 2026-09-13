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

const authService = {
  async login(data) {
    const response = await api.post("/auth/login", {
      ...data,
      device_identifier: data.device_identifier || getDeviceIdentifier(),
      platform: "web",
      device_name: navigator.userAgent.slice(0, 255),
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
    finally {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("user");
    }
  },
};

export default authService;
