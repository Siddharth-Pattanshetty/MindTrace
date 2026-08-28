import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'upload_screen.dart';
import 'practice_screen.dart';
import 'progress_screen.dart';
import 'autopsy_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _profile;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    try {
      final data = await _apiService.getStudentProfile();
      if (mounted) {
        setState(() {
          _profile = data;
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _profile = {
            "overall_health": 0.0,
            "trend": "Assessment Pending",
            "active_root_causes": []
          };
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final healthScore = (_profile?["overall_health"] as num?)?.toDouble() ?? 0.0;
    final activeCauses = List<String>.from(_profile?["active_root_causes"] ?? []);
    final activeCauseText = activeCauses.isNotEmpty ? activeCauses.first : "None (All Clean)";

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("MindTrace", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.analytics_outlined, color: Colors.cyanAccent),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ProgressScreen())),
          )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.cyanAccent))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Tagline Header
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.cyanAccent.withOpacity(0.3)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text(
                          "Don't just know what you got wrong. Discover why.",
                          style: TextStyle(fontSize: 15, fontStyle: FontStyle.italic, color: Colors.cyanAccent),
                        ),
                        SizedBox(height: 6),
                        Text(
                          "AI-Powered Forensic Learning & Diagnostic System",
                          style: TextStyle(fontSize: 12, color: Colors.white70),
                        )
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Health Status Gauge Card
                  Card(
                    color: const Color(0xFF1E293B),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Row(
                        children: [
                          Stack(
                            alignment: Alignment.center,
                            children: [
                              SizedBox(
                                width: 90,
                                height: 90,
                                child: CircularProgressIndicator(
                                  value: healthScore / 100.0,
                                  strokeWidth: 10,
                                  backgroundColor: Colors.white12,
                                  color: Colors.cyanAccent,
                                ),
                              ),
                              Text(
                                "${healthScore.toInt()}%",
                                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
                              ),
                            ],
                          ),
                          const SizedBox(width: 20),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  "Your Learning Health",
                                  style: TextStyle(fontSize: 14, color: Colors.white60),
                                ),
                                const SizedBox(height: 4),
                                Row(
                                  children: [
                                    const Icon(Icons.trending_up, color: Colors.greenAccent, size: 20),
                                    const SizedBox(width: 6),
                                    Text(
                                      _profile?["trend"] ?? "Improving",
                                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.greenAccent),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  "Active Root Cause: $activeCauseText",
                                  style: const TextStyle(fontSize: 12, color: Colors.amberAccent),
                                )
                              ],
                            ),
                          )
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 28),

                  // Action Buttons
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.cyanAccent,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.document_scanner),
                          label: const Text("Analyze Exam", style: TextStyle(fontWeight: FontWeight.bold)),
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const UploadScreen())),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: Colors.cyanAccent,
                            side: const BorderSide(color: Colors.cyanAccent),
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.model_training),
                          label: const Text("Practice Weak Areas", style: TextStyle(fontWeight: FontWeight.bold)),
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PracticeScreen())),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 28),

                  // Recent Exam Shortcut
                  const Text("Diagnostic Assessments", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 12),
                  ListTile(
                    tileColor: const Color(0xFF1E293B),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    leading: const CircleAvatar(backgroundColor: Colors.redAccent, child: Icon(Icons.bug_report, color: Colors.white)),
                    title: const Text("Mathematics Diagnostic Benchmark", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                    subtitle: const Text("Run forensic error autopsy & prerequisite gap analysis", style: TextStyle(color: Colors.white60, fontSize: 12)),
                    trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AutopsyScreen(examId: 1))),
                  ),
                ],
              ),
            ),
    );
  }
}
