import 'package:flutter/material.dart';
import 'waiter_screen.dart';
import 'kitchen_screen.dart';

class RoleSelector extends StatelessWidget {
  const RoleSelector({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text("POS SAMURAI")),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton.icon(
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const WaiterScreen())),
                icon: const Icon(Icons.restaurant),
                label: const Text("👨‍🍳 MODO MESERO"),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const KitchenScreen())),
                icon: const Icon(Icons.local_fire_department),
                label: const Text("🔥 MODO COCINA"),
              ),
            ],
          ),
        ),
      );
}
