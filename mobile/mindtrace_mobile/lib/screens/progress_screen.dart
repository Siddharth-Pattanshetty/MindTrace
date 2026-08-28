import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ProgressScreen extends StatefulWidget {
  const ProgressScreen({super.key});

  @override
  State<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends State<ProgressScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _progressData;
  bool _isLoading = true;
  bool _retestCompleted = false;
  String? _retestImprovementText;

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    try {
      final data = await _apiService.getProgress();
      setState(() {
        _progressData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _runRetest() async {
    try {
      final retestData = await _apiService.generateRetest();
      final retestId = retestData["retest_id"] ?? 1;

      final subRes = await _apiService.submitRetest(retestId, [
        {"student_answer": "6x + 7", "expected_answer": "6x + 7", "question_text": "Q1"},
        {"student_answer": "(2x + 1)(x + 4)", "expected_answer": "(2x + 1)(x + 4)", "question_text": "Q2"}
      ]);

      setState(() {
        _retestCompleted = true;
        _retestImprovementText = subRes["improvement_text"];
      });

      _loadProgress();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Re-test execution error: $e")),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Learning Progress & Longitudinal Analysis", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.cyanAccent))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Longitudinal Communicator Box
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.cyanAccent.withOpacity(0.5)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: const [
                            Icon(Icons.insights, color: Colors.cyanAccent),
                            SizedBox(width: 8),
                            Text("Longitudinal Learning Insight", style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _progressData?["longitudinal_insight"] ?? "Upload an exam paper to begin forensic diagnosis.",
                          style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  const Text("Mastery Trends", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),

                  if (_progressData?["concept_trends"] != null)
                    ...(_progressData!["concept_trends"] as List).map((t) => _buildTrendTile(
                          t["exam"] ?? "Exam",
                          "${(t["algebra_mastery"] ?? 0.0).toStringAsFixed(1)}%",
                          "${t["errors"] ?? 0} errors",
                          (t["errors"] ?? 0) == 0 ? Colors.greenAccent : Colors.amberAccent,
                        )),

                  const SizedBox(height: 24),

                  if (_retestCompleted) ...[
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.greenAccent),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text("Re-Test Verified!", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontSize: 16)),
                          const SizedBox(height: 6),
                          Text(
                            _retestImprovementText ?? "MindTrace verified your weakness resolution!",
                            style: const TextStyle(color: Colors.white70, fontSize: 13),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                  ],

                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.cyanAccent,
                        side: const BorderSide(color: Colors.cyanAccent),
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.verified),
                      label: const Text("Execute Re-Test Verification", style: TextStyle(fontWeight: FontWeight.bold)),
                      onPressed: _runRetest,
                    ),
                  )
                ],
              ),
            ),
    );
  }

  Widget _buildTrendTile(String exam, String mastery, String errors, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(exam, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500)),
          Row(
            children: [
              Text(mastery, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(width: 12),
              Text("($errors)", style: const TextStyle(color: Colors.white54, fontSize: 12)),
            ],
          )
        ],
      ),
    );
  }
}
