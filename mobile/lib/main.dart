import 'package:flutter/material.dart';
import 'config.dart';
import 'services/isar_service.dart';
import 'screens/role_selector.dart';
import 'screens/setup_screen.dart';
void main() async { WidgetsFlutterBinding.ensureInitialized(); await AppConfig.init(); await IsarService.init(); runApp(const POSApp()); }
class POSApp extends StatelessWidget { const POSApp({super.key}); @override Widget build(BuildContext context) { final isDefault = AppConfig.baseUrl.contains("192.168.1.100"); return MaterialApp(home: isDefault ? const SetupScreen() : const RoleSelector(), debugShowCheckedModeBanner: false); } }
