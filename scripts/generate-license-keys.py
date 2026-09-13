from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

root = Path(__file__).resolve().parents[1] / "local-secrets" / "licensing"
root.mkdir(parents=True, exist_ok=True)
private = Ed25519PrivateKey.generate()
(root / "private.pem").write_bytes(private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
(root / "public.pem").write_bytes(private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
print(f"Generated development license keys in {root}")
