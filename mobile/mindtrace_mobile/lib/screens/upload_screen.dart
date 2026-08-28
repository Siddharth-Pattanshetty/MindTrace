import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'autopsy_screen.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _titleController = TextEditingController(text: "Mathematics Diagnostic Exam");
  final TextEditingController _textController = TextEditingController();
  
  bool _isProcessing = false;
  String _currentStep = "";
  double _progress = 0.0;
  String? _errorMsg;

  Future<void> _startProcessing() async {
    setState(() {
      _isProcessing = true;
      _errorMsg = null;
      _currentStep = "Extracting questions via Document Processor...";
      _progress = 0.25;
    });

    try {
      await Future.delayed(const Duration(milliseconds: 500));
      setState(() {
        _currentStep = "Evaluating answers with SymPy verifier...";
        _progress = 0.55;
      });

      await Future.delayed(const Duration(milliseconds: 500));
      setState(() {
        _currentStep = "Finding root learning gaps (Prerequisite graph traversal)...";
        _progress = 0.85;
      });

      final res = await _apiService.uploadExam(
        _titleController.text,
        "Mathematics",
        _textController.text
      );

      setState(() {
        _progress = 1.0;
        _currentStep = "Analysis complete!";
      });

      await Future.delayed(const Duration(milliseconds: 200));
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => AutopsyScreen(examId: res["id"])),
        );
      }
    } catch (e) {
      setState(() {
        _isProcessing = false;
        _errorMsg = "Exam processing failed: ${e.toString().replaceAll('Exception:', '')}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Upload Exam", style: TextStyle(color: Colors.white)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (_errorMsg != null) ...[
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.red.withOpacity(0.2), borderRadius: BorderRadius.circular(8)),
                child: Text(_errorMsg!, style: const TextStyle(color: Colors.redAccent, fontSize: 13)),
              ),
              const SizedBox(height: 16),
            ],

            TextField(
              controller: _titleController,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: "Exam Title",
                labelStyle: TextStyle(color: Colors.white60),
                enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
                focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.cyanAccent)),
              ),
            ),
            const SizedBox(height: 16),
            
            // Camera / Image Upload Dropzone Simulation
            GestureDetector(
              onTap: _isProcessing ? null : _startProcessing,
              child: Container(
                height: 160,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.cyanAccent.withOpacity(0.5), style: BorderStyle.solid),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.cloud_upload_outlined, size: 48, color: Colors.cyanAccent),
                    SizedBox(height: 8),
                    Text("Tap to Upload Exam Paper / Camera Capture", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text("Supports Image, PDF, or Handwritten Sheets", style: TextStyle(color: Colors.white54, fontSize: 12)),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),
            const Text("Or paste raw exam text:", style: TextStyle(color: Colors.white70)),
            const SizedBox(height: 8),
            TextField(
              controller: _textController,
              maxLines: 4,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                hintText: "Question 1: Simplify 3(x+4) - 2(x-1)...\nStudent Answer: x + 14",
                hintStyle: TextStyle(color: Colors.white30),
                enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
                focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.cyanAccent)),
              ),
            ),

            const SizedBox(height: 24),

            if (_isProcessing) ...[
              LinearProgressIndicator(value: _progress, color: Colors.cyanAccent, backgroundColor: Colors.white12),
              const SizedBox(height: 12),
              Center(
                child: Text(
                  _currentStep,
                  style: const TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.w500),
                ),
              ),
            ] else ...[
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.cyanAccent,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _startProcessing,
                  child: const Text("Process & Analyze Exam", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              )
            ]
          ],
        ),
      ),
    );
  }
}
