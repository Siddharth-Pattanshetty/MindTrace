import 'package:flutter/material.dart';

class ProcessingScreen extends StatelessWidget {
  final String currentStep;
  final double progress;

  const ProcessingScreen({
    super.key,
    required this.currentStep,
    required this.progress,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.document_scanner_outlined, size: 80, color: Colors.cyanAccent),
            const SizedBox(height: 24),
            const Text(
              "Processing Exam Document",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 8),
            Text(
              currentStep,
              style: const TextStyle(color: Colors.cyanAccent, fontSize: 14),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            LinearProgressIndicator(
              value: progress,
              color: Colors.cyanAccent,
              backgroundColor: Colors.white12,
            ),
          ],
        ),
      ),
    );
  }
}
