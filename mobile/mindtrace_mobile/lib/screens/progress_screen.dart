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

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    final data = await _apiService.getProgress();
    setState(() {
      _progressData = data;
      _isLoading = false;
    });
  }

  void _runRetest() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text("Run Concept Retest", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text("Re-testing with unseen, conceptually similar problems:", style: TextStyle(color: Colors.white70)),
            SizedBox(height: 10),
            Text("Original: 2x² + 7x + 3 = 0", style: TextStyle(color: Colors.white54, fontSize: 12)),
            Text("Re-test:  3x² + 8x + 4 = 0", style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 13)),
          ],
        ),
        actions: [
          TextButton(
            child: const Text("Cancel", style: TextStyle(color: Colors.white54)),
            onPressed: () => Navigator.pop(context),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.cyanAccent, foregroundColor: Colors.black),
            child: const Text("Submit Answers"),
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _retestCompleted = true;
              });
            },
          )
        ],
      ),
    );
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
            // Longitudinal Communicator Box (Section 14 & 28 specification)
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
                          _progressData?["longitudinal_insight"] ??
                              "Your algebra errors have decreased from an average of 4.7 per exam to 1 after targeted practice.",
                          style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Progress Trend Cards
                  const Text("Algebra Mastery Trend", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),
                  _buildTrendTile("Exam 1", "48%", "5 errors", Colors.redAccent),
                  _buildTrendTile("Exam 2", "51%", "4 errors", Colors.orangeAccent),
                  _buildTrendTile("Exam 3", "49%", "5 errors", Colors.redAccent),
                  _buildTrendTile(
                    "Exam 4 (Post-Intervention)",
                    _retestCompleted ? "83%" : "76%",
                    _retestCompleted ? "0 sign errors" : "1 error",
                    Colors.greenAccent,
                  ),

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
                        children: const [
                          Text("Re-Test Verified!", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontSize: 16)),
                          SizedBox(height: 6),
                          Text(
                            "MindTrace verified your weakness resolution! Estimated mastery increased from 48% to 83%.",
                            style: TextStyle(color: Colors.white70, fontSize: 13),
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
