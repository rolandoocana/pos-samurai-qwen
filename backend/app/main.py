from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from . import ws_manager, router_orders, router_clients, router_products, router_cash
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
app = FastAPI(title="POS SAMURAI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")
app.include_router(router_orders.router)
app.include_router(router_clients.router)
app.include_router(router_products.router)
app.include_router(router_cash.router)
@app.on_event("startup")
def startup(): init_db()
@app.websocket("/ws/{role}")
async def ws(ws: WebSocket, role: str):
    await ws_manager.connect(ws, role)
    try:
        while True: data = await ws.receive_json(); await ws_manager.handle(ws, data, role)
    except WebSocketDisconnect: ws_manager.disconnect(ws, role)
