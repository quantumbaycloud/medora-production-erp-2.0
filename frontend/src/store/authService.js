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

const platform = () => (isElectron() ? "windows" : "web");

const authService = {
  async login(data) {
    const identifier = String(data.identifier || "").trim();
    const password = String(data.password || "");

    if (!identifier || !password) {
      throw new Error("ERP username, email or mobile number and password are required.");
    }

    const response = await api.post("/auth/login", {
      identifier,
      password,
      device_identifier: getDeviceIdentifier(),
      platform: platform(),
      device_name: isElectron()
        ? `MEDORAX ERP Windows Desktop (${navigator.userAgent.slice(0, 100)})`
        : `MEDORAX ERP Web (${navigator.userAgent.slice(0, 180)})`,
      app_version: isElectron() ? "2.0.1" : undefined,
    });

    const result = response.data || {};

    if (!result.access_token || !result.refresh_token || !result.user) {
      throw new Error("ERP authentication service returned an incomplete login response.");
    }

    localStorage.setItem("accessToken", result.access_token);
    localStorage.setItem("refreshToken", result.refresh_token);
    localStorage.setItem(
      "medorax.erp.device_id",
      result.device_identifier || getDeviceIdentifier(),
    );
    localStorage.setItem("user", JSON.stringify(result.user));

    return response;
  },

  async refresh() {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) throw new Error("No refresh token");

    const response = await api.post("/auth/refresh", {
      refresh_token: refreshToken,
    });

    const data = response.data || {};
    if (!data.access_token || !data.refresh_token) {
      throw new Error("Session refresh failed.");
    }

    localStorage.setItem("accessToken", data.access_token);
    localStorage.setItem("refreshToken", data.refresh_token);
    if (data.user) localStorage.setItem("user", JSON.stringify(data.user));

    return response;
  },

  async logout() {
    try {
      return await api.post("/auth/logout");
    } finally {
      clearAuth();
    }
  },
};

export function clearAuth() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("user");
}

export default authService;
