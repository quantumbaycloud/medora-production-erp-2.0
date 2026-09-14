"""Development-only bootstrap for a local commercial ERP installation.

This module is intentionally blocked in production. It creates a signed local
license through the local issuer and provisions one ERP account through the
normal internal provisioning contract. It does not add a registration UI.
"""
import os
import secrets
import time
import uuid

import httpx


def main() -> None:
    if os.getenv("APP_ENV", "development").lower() == "production":
        raise SystemExit("dev_bootstrap is disabled when APP_ENV=production")

    issuer = os.getenv("LOCAL_BOOTSTRAP_ISSUER_URL", os.getenv("LICENSE_ISSUER_URL", "http://licensing-issuer:8100")).rstrip("/")
    erp = os.getenv("LOCAL_BOOTSTRAP_ERP_URL", "http://erp-api:8000").rstrip("/")
    issuer_token = os.getenv("LICENSE_ISSUER_TOKEN", "")
    provision_token = os.getenv("ERP_PROVISION_TOKEN", "")
    if not issuer_token or not provision_token:
        raise SystemExit("Supply LICENSE_ISSUER_TOKEN and ERP_PROVISION_TOKEN only for this local bootstrap command")

    tenant_id = os.getenv("LOCAL_TENANT_ID", str(uuid.uuid4()))
    username = os.getenv("LOCAL_ERP_USERNAME", "demo")
    password = os.getenv("LOCAL_ERP_PASSWORD", "ChangeMe123!")
    email = os.getenv("LOCAL_ERP_EMAIL", "demo@medorax.local")
    name = os.getenv("LOCAL_ERP_NAME", "MEDORAX Demo")
    days = int(os.getenv("LOCAL_LICENSE_DAYS", "365"))
    max_devices = int(os.getenv("LOCAL_LICENSE_MAX_DEVICES", "3"))
    modules = [x.strip() for x in os.getenv("LOCAL_LICENSE_MODULES", "core,inventory,billing,purchases,reports,staff,customers,prescriptions").split(",") if x.strip()]

    payload = {
        "tenant_id": tenant_id,
        "plan": os.getenv("LOCAL_LICENSE_PLAN", "commercial-dev"),
        "expires_at": int(time.time()) + days * 86400,
        "max_devices": max_devices,
        "modules": modules,
    }

    with httpx.Client(timeout=20) as client:
        issued = client.post(f"{issuer}/v1/licenses", json=payload, headers={"X-Issuer-Token": issuer_token})
        issued.raise_for_status()
        envelope = issued.json()

        license_payload = envelope["license"]
        provision = {
            "licenseKey": license_payload["license_id"],
            "licenseExpiresAt": license_payload["expires_at"],
            "license": license_payload,
            "licenseSignature": envelope["signature"],
            "pharmacyId": tenant_id,
            "erpUsername": username,
            "temporaryPassword": password,
            "user": {"name": name, "email": email},
            "business": {"name": "MEDORAX Demo Pharmacy", "contact_email": email},
        }
        response = client.post(
            f"{erp}/internal/erp/provision",
            json=provision,
            headers={"Authorization": f"Bearer {provision_token}"},
        )
        response.raise_for_status()

    print("Local ERP provisioned successfully")
    print(f"Tenant/Pharmacy ID: {tenant_id}")
    print(f"ERP username:       {username}")
    print(f"ERP password:       {password}")
    print(f"License ID:         {license_payload['license_id']}")


if __name__ == "__main__":
    main()
