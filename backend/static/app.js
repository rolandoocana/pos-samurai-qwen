let ws; const role = location.pathname.includes("kitchen") ? "kitchen" : location.pathname.includes("admin") ? "admin" : "cashier";
function connect() {
  ws = new WebSocket(`ws://${location.host}/ws/${role}`);
  ws.onopen = () => { const s = document.getElementById("status"); if(s) s.textContent = "✅ Online"; };
  ws.onmessage = e => { const d = JSON.parse(e.data); if(role==="kitchen" && d.type==="new_order") renderOrder(d); if(role==="admin" && d.type==="price_refresh") loadProducts(); };
  ws.onclose = setTimeout(connect, 3000);
}
async function api(url, opts={}) { const res = await fetch(url, {headers:{"Content-Type":"application/json"}, ...opts}); return res.json(); }
async function pay(oid, method="CASH", doc="") { await api(`/api/orders/${oid}/pay`, {method:"POST", body:JSON.stringify({method, amount:0, client_doc:doc})}); alert("✅ Cobrado. Imprimiendo..."); }
function renderOrder(d) { const grid = document.getElementById("grid"); if(!grid) return; grid.insertAdjacentHTML("beforeend", `<div class="card"><h3>Mesa ${d.table||'LLEVAR'}</h3><div class="notes">⚠️ SIN SAL, BIEN COCIDO</div><button onclick="this.parentElement.style.background='#4caf50'">✅ LISTO</button></div>`); }
async function loadProducts(){ if(document.getElementById('tbody')){ const res=await fetch('/api/products'); const p=await res.json(); document.getElementById('tbody').innerHTML=p.map(x=>`<tr><td>${x.name}</td><td>$${x.price.toFixed(2)}</td><td><input type='number' step='0.01' value='${x.price}' onchange='chg("${x.id}",this.value)'></td></tr>`).join(''); }}
connect();
