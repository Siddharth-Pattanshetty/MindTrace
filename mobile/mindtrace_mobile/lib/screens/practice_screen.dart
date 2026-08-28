import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'progress_screen.dart';

class PracticeScreen extends StatefulWidget {
  const PracticeScreen({super.key});

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _answerController = TextEditingController();

  int _currentIndex = 0;
  bool _submitted = false;
  Map<String, dynamic>? _lastFeedback;

  final List<Map<String, String>> _questions = [
    {
      "question": "Simplify the expression: 4(2x - 5) - 3(x - 2)",
      "expected": "5x - 14",
      "concept": "Algebraic Manipulation"
    },
    {
      "question": "Factorize completely: x^2 + 8x + 15",
      "expected": "(x + 3)(x + 5)",
      "concept": "Factorization"
    },
    {
      "question": "Solve the quadratic equation: 2x^2 + 7x + 3 = 0",
      "expected": "x = -1/2, x = -3",
      "concept": "Quadratic Equations"
    },
    {
      "question": "Factorize completely: 3x^2 + 8x + 4",
      "expected": "(3x + 2)(x + 2)",
      "concept": "Factorization"
    },
    {
      "question": "Solve for x: 5(x - 3) = 2(x + 6)",
      "expected": "x = 9",
      "concept": "Equations"
    }
  ];

  Future<void> _submitAnswer() async {
    if (_answerController.text.trim().isEmpty) return;

    final result = await _apiService.submitPracticeAttempt(
      _currentIndex + 1,
      _answerController.text.trim(),
    );

    setState(() {
      _submitted = true;
      _lastFeedback = result;
    });
  }

  void _nextQuestion() {
    if (_currentIndex < _questions.length - 1) {
      setState(() {
        _currentIndex++;
        _submitted = false;
        _lastFeedback = null;
        _answerController.clear();
      });
    } else {
      // Completed practice set, push to Retest / Progress Screen
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const ProgressScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final q = _questions[_currentIndex];

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        title: const Text("Targeted Practice", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E293B),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Info
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text("Weakness: Factorization", style: TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold)),
                Text("Progress: ${_currentIndex + 1}/${_questions.length}", style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(
              value: (_currentIndex + 1) / _questions.length,
              color: Colors.cyanAccent,
              backgroundColor: Colors.white12,
            ),

            const SizedBox(height: 24),

            // Question Card
            Card(
              color: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("Question ${_currentIndex + 1}", style: const TextStyle(color: Colors.white54, fontSize: 13)),
                    const SizedBox(height: 8),
                    Text(
                      q["question"]!,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Answer Input Field
            TextField(
              controller: _answerController,
              enabled: !_submitted,
              style: const TextStyle(color: Colors.white, fontSize: 16),
              decoration: const InputDecoration(
                labelText: "Your Answer",
                hintText: "e.g. 5x - 14",
                labelStyle: TextStyle(color: Colors.white60),
                hintStyle: TextStyle(color: Colors.white30),
                enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
                focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Colors.cyanAccent)),
              ),
            ),

            const SizedBox(height: 20),

            if (!_submitted)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.cyanAccent,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _submitAnswer,
                  child: const Text("Submit", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              )
            else ...[
              // Feedback Panel (Section 27 specification)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: (_lastFeedback?["is_correct"] ?? false)
                      ? Colors.green.withOpacity(0.15)
                      : Colors.red.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: (_lastFeedback?["is_correct"] ?? false) ? Colors.greenAccent : Colors.redAccent,
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          (_lastFeedback?["is_correct"] ?? false) ? Icons.check_circle : Icons.error,
                          color: (_lastFeedback?["is_correct"] ?? false) ? Colors.greenAccent : Colors.redAccent,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          (_lastFeedback?["is_correct"] ?? false) ? "Correct" : "Incorrect",
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: (_lastFeedback?["is_correct"] ?? false) ? Colors.greenAccent : Colors.redAccent,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "Why: ${_lastFeedback?["explanation"] ?? "Detailed explanation"}",
                      style: const TextStyle(color: Colors.white70, fontSize: 13),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      "Error pattern: No recurring sign error detected.",
                      style: TextStyle(color: Colors.cyanAccent, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "Mastery updated: 52% → ${(_lastFeedback?["updated_mastery"] ?? 61).toInt()}%",
                      style: const TextStyle(color: Colors.amberAccent, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _nextQuestion,
                  child: Text(
                    _currentIndex < _questions.length - 1 ? "Next Question" : "Complete & Run Re-Test",
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
