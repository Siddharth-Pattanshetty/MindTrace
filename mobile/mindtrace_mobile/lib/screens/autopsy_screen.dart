import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'root_cause_screen.dart';
import 'practice_screen.dart';

class AutopsyScreen extends StatefulWidget {
  final int examId;
  const AutopsyScreen({super.key, required this.examId});

  @override
  State<AutopsyScreen> createState() => _AutopsyScreenState();
}

class _AutopsyScreenState extends State<AutopsyScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _analysis;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAnalysis();
  }

  Future<void> _loadAnalysis() async {
    final data = await _apiService.getExamAnalysis(widget.examId);
    setState(() {
      _analysis = data;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Exam Autopsy", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.cyanAccent))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Score Overview Card
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: Colors.redAccent.withOpacity(0.4)),
                    ),
                    child: Column(
                      children: [
                        const Text("Score", style: TextStyle(color: Colors.white60, fontSize: 14)),
                        const SizedBox(height: 6),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.baseline,
                          textBaseline: TextBaseline.alphabetic,
                          children: [
                            Text(
                              "${(_analysis?["score"] ?? 62).toInt()}",
                              style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.redAccent),
                            ),
                            Text(
                              " / ${(_analysis?["max_score"] ?? 100).toInt()}",
                              style: const TextStyle(fontSize: 20, color: Colors.white54),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        const Text("7 Incorrect Answers Identified", style: TextStyle(color: Colors.amberAccent, fontSize: 13, fontWeight: FontWeight.w500)),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Error Taxonomy Breakdown
                  const Text("Errors Breakdown", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      _buildErrorCard("Concept errors", "${_analysis?["error_counts"]?["concept_errors"] ?? 18}", Colors.purpleAccent),
                      const SizedBox(width: 8),
                      _buildErrorCard("Calculation errors", "${_analysis?["error_counts"]?["calculation_errors"] ?? 8}", Colors.orangeAccent),
                      const SizedBox(width: 8),
                      _buildErrorCard("Procedural errors", "${_analysis?["error_counts"]?["procedural_errors"] ?? 7}", Colors.blueAccent),
                    ],
                  ),

                  const SizedBox(height: 24),

                  // Proprietary Root Cause Banner
                  Card(
                    color: const Color(0xFF1E293B),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                      side: const BorderSide(color: Colors.cyanAccent, width: 1.5),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const Text("Root Cause", style: TextStyle(color: Colors.white70, fontSize: 14)),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                decoration: BoxDecoration(
                                  color: Colors.cyanAccent.withOpacity(0.2),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  "${((_analysis?["confidence"] ?? 0.91) * 100).toInt()}% diagnostic confidence",
                                  style: const TextStyle(color: Colors.cyanAccent, fontSize: 11, fontWeight: FontWeight.bold),
                                ),
                              )
                            ],
                          ),
                          const SizedBox(height: 10),
                          Text(
                            _analysis?["root_cause"] ?? "Weak Algebraic Manipulation",
                            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            _analysis?["summary"] ?? "Identified recurring sign and factorization error patterns.",
                            style: const TextStyle(color: Colors.white60, fontSize: 13),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 28),

                  // Action Buttons
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: Colors.cyanAccent,
                            side: const BorderSide(color: Colors.cyanAccent),
                            padding: const EdgeInsets.symmetric(vertical: 14),
                          ),
                          icon: const Icon(Icons.info_outline),
                          label: const Text("View Root Cause"),
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RootCauseScreen())),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.cyanAccent,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                          ),
                          icon: const Icon(Icons.play_arrow),
                          label: const Text("Start Practice", style: TextStyle(fontWeight: FontWeight.bold)),
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PracticeScreen())),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
    );
  }

  Widget _buildErrorCard(String title, String count, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
        decoration: BoxDecoration(
          color: const Color(0xFF1E293B),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Text(count, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 4),
            Text(title, textAlign: TextAlign.center, style: const TextStyle(fontSize: 10, color: Colors.white60)),
          ],
        ),
      ),
    );
  }
}
