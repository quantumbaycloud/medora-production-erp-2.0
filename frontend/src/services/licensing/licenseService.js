import api from "../api";
import { getDeviceIdentifier } from "../../store/authService";

export const getDeviceId = getDeviceIdentifier;

const deviceName = () =>
  typeof navigator !== "undefined"
    ? navigator.userAgent.slice(0, 255)
    : "MEDORAX ERP";

const licenseService = {
  status(token, tenantId) {
    return api.get("/api/licensing/status", {
      params: {
        tenant_id: tenantId,
        device_id: getDeviceId(),
      },
    });
  },

  provisioned(token, tenantId) {
    return api.get("/api/licensing/provisioned", {
      params: {
        tenant_id: tenantId,
      },
    });
  },

  activateByKey(token, licenseKey, tenantId) {
    return api.post(
      "/api/licensing/activate-key",
      {
        license_key: licenseKey.trim(),
      },
      {
        params: {
          tenant_id: tenantId,
        },
      },
    );
  },

  bootstrap(token, tenantId, name = deviceName()) {
    return api.post(
      "/api/licensing/bootstrap-device",
      {
        device_id: getDeviceId(),
        device_name: name,
      },
      {
        params: {
          tenant_id: tenantId,
        },
      },
    );
  },

  activate(token, envelope, tenantId, name = deviceName()) {
    return api.post(
      "/api/licensing/activate",
      {
        ...envelope,
        device_id: getDeviceId(),
        device_name: name,
      },
      {
        params: {
          tenant_id: tenantId,
        },
      },
    );
  },

  deactivate(token, tenantId) {
    return api.post(
      "/api/licensing/deactivate",
      {
        device_id: getDeviceId(),
      },
      {
        params: {
          tenant_id: tenantId,
        },
      },
    );
  },

  refresh(token, tenantId) {
    return api.post(
      "/api/licensing/refresh",
      null,
      {
        params: {
          tenant_id: tenantId,
          device_id: getDeviceId(),
        },
      },
    );
  },
};

export default licenseService;