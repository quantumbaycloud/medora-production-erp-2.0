import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

const api = axios.create({
  baseURL,
  timeout: Number(import.meta.env.VITE_API_TIMEOUT_MS || 30000),
  headers: { "Content-Type": "application/json" },
});

let refreshPromise = null;

function clearAuth() {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("user");
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error?.response?.status;
    const original = error?.config;
    if (status !== 401 || !original || original._retry || original.url?.includes("/auth/refresh")) {
      return Promise.reject(error);
    }

    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      clearAuth();
      return Promise.reject(error);
    }

    original._retry = true;
    try {
      if (!refreshPromise) {
        refreshPromise = axios.post(`${baseURL}/auth/refresh`, { refresh_token: refreshToken }, {
          timeout: 15000,
          headers: { "Content-Type": "application/json" },
        }).then((response) => {
          const data = response.data || {};
          if (!data.access_token) throw new Error("Refresh response did not contain an access token");
          localStorage.setItem("accessToken", data.access_token);
          if (data.refresh_token) localStorage.setItem("refreshToken", data.refresh_token);
          return data.access_token;
        }).finally(() => {
          refreshPromise = null;
        });
      }
      const token = await refreshPromise;
      original.headers.Authorization = `Bearer ${token}`;
      return api(original);
    } catch (refreshError) {
      clearAuth();
      return Promise.reject(refreshError);
    }
  },
);

export const getActivePharmacyId = () => localStorage.getItem("medorax.erp.pharmacy_id");
export const setActivePharmacyId = (id) => {
  if (id) localStorage.setItem("medorax.erp.pharmacy_id", id);
  else localStorage.removeItem("medorax.erp.pharmacy_id");
};

export const withPharmacy = (params = {}) => ({
  ...params,
  ...(getActivePharmacyId() ? { pharmacy_id: getActivePharmacyId() } : {}),
});

export default api;
