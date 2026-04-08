from fastapi import WebSocket
connections = {"kitchen": [], "cashier": [], "waiter": []}
async def connect(ws: WebSocket, role: str): await ws.accept(); connections.setdefault(role, []).append(ws)
def disconnect(ws: WebSocket, role: str): 
    if ws in connections.get(role, []): connections[role].remove(ws)
async def broadcast(roles: list, data: dict):
    for role in roles:
        dead = []
        for ws in connections.get(role, []):
            try: await ws.send_json(data)
            except: dead.append(ws)
        for ws in dead: connections[role].remove(ws)
async def handle(ws: WebSocket, data: dict, role: str):
    if data.get("type") in ["item_status", "new_order"]: await broadcast(["kitchen", "cashier"], data)
    elif data.get("type") in ["price_updated", "price_refresh"]: await broadcast(["kitchen", "cashier", "waiter"], data)
