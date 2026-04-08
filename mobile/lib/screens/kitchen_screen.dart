import 'package:flutter/material.dart';
import '../services/ws_service.dart';
import '../services/api_service.dart';

class KitchenScreen extends StatefulWidget {
  const KitchenScreen({super.key});

  @override
  State<KitchenScreen> createState() => _KitchenScreenState();
}

class _KitchenScreenState extends State<KitchenScreen> {
  final List<Map<String, dynamic>> orders = [];

  @override
  void initState() {
    super.initState();
    WsService.connect("kitchen", (msg) {
      if (msg["type"] == "new_order") {
        setState(() {
          orders.add({
            "id": msg["order_id"],
            "table": msg["table"] ?? "LLEVAR",
            "time": DateTime.now().toString().substring(11, 16),
            "notes": ["PEDIDO NUEVO"]
          });
        });
      }
    });
  }

  void _markReady(String id) {
    ApiService.updateItemStatus(id, "READY");
    setState(() {
      orders.removeWhere((o) => o["id"] == id);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black87,
      appBar: AppBar(
        title: const Text("🔥 COCINA", style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.red[900],
      ),
      body: orders.isEmpty
          ? const Center(child: Text("Sin pedidos", style: TextStyle(color: Colors.white70, fontSize: 20)))
          : Padding(
              padding: const EdgeInsets.all(12),
              child: Wrap(
                spacing: 12,
                runSpacing: 12,
                children: orders.map((o) {
                  return Container(
                    width: 280,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.grey[900],
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.red[700]!, width: 2),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "MESA ",
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
                            ),
                            Text(o["time"], style: const TextStyle(color: Colors.grey)),
                          ],
                        ),
                        const Divider(color: Colors.grey),
                        const Spacer(),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton.icon(
                            onPressed: () => _markReady(o["id"]),
                            icon: const Icon(Icons.check),
                            label: const Text("✅ LISTO"),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                              padding: const EdgeInsets.symmetric(vertical: 12),
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),
    );
  }
}
