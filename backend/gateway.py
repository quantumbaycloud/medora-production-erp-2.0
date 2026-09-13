from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Medorax API Gateway")

# Explicitly define allowed frontend domains (Both localhost and 127.0.0.1)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dual-network layout resolution mapping constants
CORE_URL = "http://127.0.0.1:8000"
INVENTORY_URL = "http://127.0.0.1:8001"
FINANCE_URL = "http://127.0.0.1:8002"

# Persistent async client for request pooling
client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    """Closes the underlying HTTPX connection pool gracefully on gateway exit"""
    await client.aclose()

def clean_proxy_headers(response_headers: dict) -> dict:
    """Removes transport-specific headers from the microservice response 
    to let the Gateway's ASGI server and CORS layer manage them safely."""
    headers = dict(response_headers)
    headers.pop("content-length", None)
    headers.pop("content-encoding", None)
    headers.pop("transfer-encoding", None)
    headers.pop("connection", None)
    return headers

@app.api_route("/finance/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_finance(request: Request, path: str):
    """Forwards all /finance/... traffic to the Financial System microservice on port 8002"""
    clean_path = path.strip("/")
    url = f"{FINANCE_URL}/finance/{clean_path}/" if clean_path else f"{FINANCE_URL}/finance/"
    body = await request.body()
    
    try:
        proxy_req = client.build_request(
            request.method, url, headers=request.headers.raw, content=body, params=request.query_params
        )
        response = await client.send(proxy_req)
        headers = clean_proxy_headers(response.headers)
        return Response(content=response.content, status_code=response.status_code, headers=headers)
    except httpx.ConnectError:
        return Response(
            content='{"error": "Finance microservice is offline or unreachable."}',
            status_code=503,
            media_type="application/json"
        )

@app.api_route("/inventory/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_inventory(request: Request, path: str):
    """
    Forwards traffic ensuring the microservice receives a clean routing structure.
    Safely escapes explicit view paths to bypass DRF router collection bottlenecks.
    """
    clean_path = path.strip("/")
    
    # ─── EXTRA STRAP ESCAPE GATES (Guarantees absolute route lookup safety) ───
    if "available-stock" in clean_path:
        url = f"{INVENTORY_URL}/inventory/available-stock/"
    elif "medicines" in clean_path:
        # Preserve full detail paths like medicines/<id>/batches/ and medicines/<id>/
        url = f"{INVENTORY_URL}/inventory/{clean_path}/"
    elif "verify-stock" in clean_path:
        url = f"{INVENTORY_URL}/inventory/verify-stock/"
    elif clean_path:
        # Preserve full paths including inventory/<id>/ for detail endpoints
        url = f"{INVENTORY_URL}/inventory/{clean_path}/"
    else:
        url = f"{INVENTORY_URL}/inventory/"
        
    print(f"\n🚀 GATEWAY IS FORWARDING TO DJANGO ROUTE: {url}\n")
        
    body = await request.body()
    
    try:
        proxy_req = client.build_request(
            request.method, url, headers=request.headers.raw, content=body, params=request.query_params
        )
        response = await client.send(proxy_req)
        headers = clean_proxy_headers(response.headers)
        return Response(content=response.content, status_code=response.status_code, headers=headers)
    except httpx.ConnectError:
        return Response(
            content='{"error": "Inventory microservice is offline or unreachable on port 8001."}',
            status_code=503,
            media_type="application/json"
        )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_default(request: Request, path: str):
    """Forwards all other traffic (like /suppliers/...) to the FastAPI core system on port 8000"""
    clean_path = path.strip("/")
    
    # HIGH PRIORITY ESCAPE: If the request is an inventory call that somehow slipped past the first route decorator, force-route it to port 8001
    if "inventory" in clean_path or "available-stock" in clean_path:
        segment = clean_path.replace("inventory/", "").strip("/")
        url = f"{INVENTORY_URL}/inventory/{segment}/" if segment else f"{INVENTORY_URL}/inventory/"
        print(f"\n⚡ ESCAPE LAYER FORWARDING STRAP: {url}\n")
        body = await request.body()
        try:
            proxy_req = client.build_request(request.method, url, headers=request.headers.raw, content=body, params=request.query_params)
            response = await client.send(proxy_req)
            return Response(content=response.content, status_code=response.status_code, headers=clean_proxy_headers(response.headers))
        except httpx.ConnectError:
            return Response(content='{"error": "Inventory offline via fallback link"}', status_code=503, media_type="application/json")

    url = f"{CORE_URL}/{clean_path}/" if clean_path else f"{CORE_URL}/"
    body = await request.body()
    
    try:
        proxy_req = client.build_request(
            request.method, url, headers=request.headers.raw, content=body, params=request.query_params
        )
        response = await client.send(proxy_req)
        headers = clean_proxy_headers(response.headers)
        return Response(content=response.content, status_code=response.status_code, headers=headers)
    except httpx.ConnectError:
        return Response(
            content='{"error": "Core microservice is offline or unreachable."}',
            status_code=503,
            media_type="application/json"
        )
