import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'progress_screen.dart';

class PracticeScreen extends StatefulWidget {
  final int practiceSetId;
  final String concept;
  const PracticeScreen({
    super.key,
    this.practiceSetId = 1,
    this.concept = "Factorization",
  });

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _answerController = TextEditingController();

  List<Map<String, dynamic>> _questions = [];
  int _currentIndex = 0;
  bool _isLoading = true;
  bool _submitted = false;
  Map<String, dynamic>? _lastFeedback;
  String? _errorMsg;

  @override
  void initState() {
    super.initState();
    _loadPracticeSet();
  }

  Future<void> _loadPracticeSet() async {
    try {
      final res = await _apiService.generatePracticeSet(1, widget.concept, 5);
      final qList = List<Map<String, dynamic>>.from(res["questions"] ?? []);
      setState(() {
        _questions = qList;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMsg = "Failed to load practice questions: $e";
        _isLoading = false;
      });
    }
  }

  Future<void> _submitAnswer() async {
    if (_answerController.text.trim().isEmpty || _questions.isEmpty) return;

    final q = _questions[_currentIndex];
    final qId = q["id"] ?? (_currentIndex + 1);

    try {
      final result = await _apiService.submitPracticeAttempt(
        widget.practiceSetId,
        qId,
        _answerController.text.trim(),
      );

      setState(() {
        _submitted = true;
        _lastFeedback = result;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error submitting answer: $e")),
      );
    }
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
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const ProgressScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        appBar: AppBar(title: const Text("Targeted Practice"), backgroundColor: const Color(0xFF1E293B)),
        body: const Center(child: CircularProgressIndicator(color: Colors.cyanAccent)),
      );
    }

    if (_errorMsg != null || _questions.isEmpty) {
      return Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        appBar: AppBar(title: const Text("Targeted Practice"), backgroundColor: const Color(0xFF1E293B)),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Text(_errorMsg ?? "No practice questions available.", style: const TextStyle(color: Colors.redAccent)),
          ),
        ),
      );
    }

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
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text("Weakness: ${widget.concept}", style: const TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold)),
                Text("Progress: ${_currentIndex + 1}/${_questions.length}", style: const TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold)),
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
                      q["question_text"] ?? q["question"] ?? "Solve problem",
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
                  child: const Text("Submit Answer", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              )
            else ...[
              // Feedback Panel
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
                      "Why: ${_lastFeedback?["explanation"] ?? q["explanation"] ?? "Explanation"}",
                      style: const TextStyle(color: Colors.white70, fontSize: 13),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "Error detected: ${_lastFeedback?["error_detected"] ?? 'None'}",
                      style: const TextStyle(color: Colors.cyanAccent, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "Updated Estimated Mastery: ${(_lastFeedback?["updated_mastery"] ?? 50.0).toStringAsFixed(1)}%",
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
