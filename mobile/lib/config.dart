import 'package:shared_preferences/shared_preferences.dart';
class AppConfig {
  static String _baseUrl = "http://192.168.1.100:8000";
  static String get baseUrl => _baseUrl;
  static String get wsUrl => _baseUrl.replaceFirst("http", "ws");
  static Future<void> setUrl(String url) async { _baseUrl = url; final prefs = await SharedPreferences.getInstance(); await prefs.setString("lan_ip", url); }
  static Future<void> init() async { final prefs = await SharedPreferences.getInstance(); _baseUrl = prefs.getString("lan_ip") ?? _baseUrl; }
}
