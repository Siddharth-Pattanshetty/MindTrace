import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
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
  
  String? _selectedFilePath;
  String? _selectedFileName;
  int? _selectedFileSize;

  bool _isProcessing = false;
  String _currentStep = "";
  double _progress = 0.0;
  String? _errorMsg;

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.any,
      );

      if (result != null && result.files.single.path != null) {
        setState(() {
          _selectedFilePath = result.files.single.path;
          _selectedFileName = result.files.single.name;
          _selectedFileSize = result.files.single.size;
          _errorMsg = null;
        });
      }
    } catch (e) {
      setState(() {
        _errorMsg = "Failed to select file: ${e.toString()}";
      });
    }
  }

  void _clearSelectedFile() {
    setState(() {
      _selectedFilePath = null;
      _selectedFileName = null;
      _selectedFileSize = null;
    });
  }

  Future<void> _startProcessing() async {
    if ((_selectedFilePath == null || _selectedFilePath!.isEmpty) && _textController.text.trim().isEmpty) {
      setState(() {
        _errorMsg = "Please tap above to pick an exam file (PDF/Image) or paste exam text before processing.";
      });
      return;
    }

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
        _textController.text,
        filePath: _selectedFilePath,
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

  String _formatFileSize(int bytes) {
    if (bytes < 1024) return "$bytes B";
    if (bytes < 1024 * 1024) return "${(bytes / 1024).toStringAsFixed(1)} KB";
    return "${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB";
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
            
            // Image / PDF Upload Dropzone with FilePicker
            GestureDetector(
              onTap: _isProcessing ? null : _pickFile,
              child: Container(
                constraints: const BoxConstraints(minHeight: 160),
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: _selectedFilePath != null ? Colors.greenAccent : Colors.cyanAccent.withOpacity(0.5),
                    width: 1.5,
                  ),
                ),
                child: _selectedFilePath != null
                    ? Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.check_circle_outline, size: 44, color: Colors.greenAccent),
                          const SizedBox(height: 8),
                          Text(
                            _selectedFileName ?? "Selected File",
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15),
                            textAlign: TextAlign.center,
                          ),
                          if (_selectedFileSize != null) ...[
                            const SizedBox(height: 4),
                            Text(_formatFileSize(_selectedFileSize!), style: const TextStyle(color: Colors.white54, fontSize: 12)),
                          ],
                          const SizedBox(height: 12),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              OutlinedButton.icon(
                                style: OutlinedButton.styleFrom(
                                  side: const BorderSide(color: Colors.cyanAccent),
                                  foregroundColor: Colors.cyanAccent,
                                ),
                                onPressed: _isProcessing ? null : _pickFile,
                                icon: const Icon(Icons.folder_open, size: 18),
                                label: const Text("Change File"),
                              ),
                              const SizedBox(width: 12),
                              IconButton(
                                icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                                onPressed: _isProcessing ? null : _clearSelectedFile,
                                tooltip: "Remove file",
                              )
                            ],
                          )
                        ],
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.cloud_upload_outlined, size: 48, color: Colors.cyanAccent),
                          SizedBox(height: 8),
                          Text("Tap to Select Exam Paper (PDF / Image)", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          SizedBox(height: 4),
                          Text("Supports PDF, PNG, JPG, or Handwritten Scans", style: TextStyle(color: Colors.white54, fontSize: 12)),
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

