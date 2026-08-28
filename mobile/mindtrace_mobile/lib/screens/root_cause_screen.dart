import 'package:flutter/material.dart';
import 'practice_screen.dart';

class RootCauseScreen extends StatelessWidget {
  final String rootCause;
  final double confidence;
  final List<String> evidence;
  final List<String> affectedConcepts;

  const RootCauseScreen({
    super.key,
    required this.rootCause,
    required this.confidence,
    required this.evidence,
    this.affectedConcepts = const ["Expressions", "Factorization", "Equations", "Quadratics"],
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Root-Cause Explanation", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Why did you lose marks?",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 16),

            // Main Primary Weakness Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.amberAccent.withOpacity(0.5)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Primary weakness:", style: TextStyle(color: Colors.white60, fontSize: 13)),
                  const SizedBox(height: 4),
                  Text(
                    rootCause,
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.amberAccent),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      const Icon(Icons.verified, color: Colors.cyanAccent, size: 18),
                      const SizedBox(width: 6),
                      Text("MindTrace Diagnostic confidence: ${(confidence * 100).toInt()}%", style: const TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 13)),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Evidence Section
            const Text("Evidence:", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 10),
            if (evidence.isEmpty)
              const Text("No specific error patterns recorded.", style: TextStyle(color: Colors.white54))
            else
              ...evidence.map((e) => _buildEvidenceItem(e)),

            const SizedBox(height: 24),

            // Affected Concepts Chips
            const Text("Affected concepts:", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: affectedConcepts.map((c) => _buildConceptChip(c, Colors.cyanAccent)).toList(),
            ),

            const SizedBox(height: 28),

            // Prerequisite Dependency Graph
            const Text("Prerequisite Dependency Graph", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white12),
              ),
              child: Column(
                children: [
                  _buildGraphNode("Quadratic Equations", "Depends on Factorization", false),
                  const Icon(Icons.arrow_downward, color: Colors.white38),
                  _buildGraphNode("Factorization", "Depends on Algebraic Manipulation", false),
                  const Icon(Icons.arrow_downward, color: Colors.redAccent, size: 28),
                  _buildGraphNode(rootCause, "FOUNDATIONAL ROOT GAP DETECTED", true),
                  const Icon(Icons.arrow_downward, color: Colors.white38),
                  _buildGraphNode("Algebraic Expressions", "Prerequisite Concept", false),
                ],
              ),
            ),

            const SizedBox(height: 28),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.play_arrow),
                label: const Text("Start Targeted Practice", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PracticeScreen())),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildEvidenceItem(String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("• ", style: TextStyle(color: Colors.redAccent, fontSize: 18, fontWeight: FontWeight.bold)),
          Expanded(child: Text(text, style: const TextStyle(color: Colors.white70, fontSize: 14))),
        ],
      ),
    );
  }

  Widget _buildConceptChip(String name, Color color) {
    return Chip(
      backgroundColor: color.withOpacity(0.15),
      side: BorderSide(color: color.withOpacity(0.5)),
      label: Text(name, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
    );
  }

  Widget _buildGraphNode(String title, String subtitle, bool isGap) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isGap ? Colors.redAccent.withOpacity(0.2) : Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: isGap ? Colors.redAccent : Colors.white24, width: isGap ? 2 : 1),
      ),
      child: Column(
        children: [
          Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: isGap ? Colors.redAccent : Colors.white)),
          Text(subtitle, style: TextStyle(fontSize: 11, color: isGap ? Colors.amberAccent : Colors.white54)),
        ],
      ),
    );
  }
}
