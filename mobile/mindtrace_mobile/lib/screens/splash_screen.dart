import 'package:flutter/material.dart';
import 'login_screen.dart';
import 'home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const LoginScreen()),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.psychology_outlined, size: 80, color: Colors.cyanAccent),
            SizedBox(height: 16),
            Text(
              "MindTrace",
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            SizedBox(height: 8),
            Text(
              "Don't just know what you got wrong. Discover why.",
              style: TextStyle(fontSize: 14, fontStyle: FontStyle.italic, color: Colors.cyanAccent),
            ),
            SizedBox(height: 32),
            CircularProgressIndicator(color: Colors.cyanAccent),
          ],
        ),
      ),
    );
  }
}
