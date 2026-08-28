import 'package:flutter/material.dart';
import 'practice_screen.dart';

class InterventionScreen extends StatelessWidget {
  const InterventionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Personalized Intervention", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Adaptive Remediation Roadmap",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 6),
            const Text(
              "Root Cause: Weak Algebraic Manipulation",
              style: TextStyle(color: Colors.amberAccent, fontSize: 14, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 20),

            _buildLevelTile(
              level: 1,
              title: "Level 1: Basic Algebraic Manipulation & Sign Rules",
              description: "Master bracket expansion and sign distribution (e.g. -(a - b) = -a + b).",
              status: "UNLOCKED",
              isCurrent: true,
            ),
            _buildLevelTile(
              level: 2,
              title: "Level 2: Factorization & Common Terms",
              description: "Extract common algebraic terms and group quadratic expressions.",
              status: "LOCKED",
              isCurrent: false,
            ),
            _buildLevelTile(
              level: 3,
              title: "Level 3: Quadratic Equations & Equation Solving",
              description: "Apply zero-product property and solve equations with negative coefficients.",
              status: "LOCKED",
              isCurrent: false,
            ),
            _buildLevelTile(
              level: 4,
              title: "Level 4: Exam-Level Multistep Problems",
              description: "Solve multi-variable complex algebraic exam problems with zero sign errors.",
              status: "LOCKED",
              isCurrent: false,
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
                label: const Text("Start Level 1 Practice", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PracticeScreen())),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildLevelTile({
    required int level,
    required String title,
    required String description,
    required String status,
    required bool isCurrent,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isCurrent ? Colors.cyanAccent : Colors.white12,
          width: isCurrent ? 2 : 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: isCurrent ? Colors.cyanAccent : Colors.white)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: isCurrent ? Colors.cyanAccent.withOpacity(0.2) : Colors.white12,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  status,
                  style: TextStyle(fontSize: 10, color: isCurrent ? Colors.cyanAccent : Colors.white54, fontWeight: FontWeight.bold),
                ),
              )
            ],
          ),
          const SizedBox(height: 6),
          Text(description, style: const TextStyle(color: Colors.white60, fontSize: 12)),
        ],
      ),
    );
  }
}
