import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  runApp(const MindTraceApp());
}

class MindTraceApp extends StatelessWidget {
  const MindTraceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MindTrace',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.cyan,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        useMaterial3: true,
      ),
      home: const SplashScreen(),
    );
  }
}
