import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000/api";
  static String? authToken;
  static int currentUserId = 1;

  Map<String, String> get _headers => {
    "Content-Type": "application/json",
    if (authToken != null) "Authorization": "Bearer $authToken",
  };

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"email": email, "password": password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      authToken = data["access_token"];
      currentUserId = data["user_id"] ?? 1;
      return data;
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err["detail"] ?? "Login failed");
    }
  }

  Future<Map<String, dynamic>> register(String email, String password, String fullName) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"email": email, "password": password, "full_name": fullName}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final err = jsonDecode(response.body);
      throw Exception(err["detail"] ?? "Registration failed");
    }
  }

  Future<Map<String, dynamic>> uploadExam(String title, String subject, String rawText, {String? filePath}) async {
    if (filePath != null && filePath.isNotEmpty) {
      // Multipart request for real exam image/PDF upload
      var request = http.MultipartRequest('POST', Uri.parse("$baseUrl/exams/upload"));
      if (authToken != null) {
        request.headers["Authorization"] = "Bearer $authToken";
      }
      request.fields['title'] = title;
      request.fields['subject'] = subject;
      if (rawText.isNotEmpty) request.fields['raw_text'] = rawText;

      request.files.add(await http.MultipartFile.fromPath('file', filePath));
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception("Failed to upload exam file: ${response.body}");
      }
    } else {
      final response = await http.post(
        Uri.parse("$baseUrl/exams/upload"),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          if (authToken != null) "Authorization": "Bearer $authToken",
        },
        body: {
          "title": title,
          "subject": subject,
          "raw_text": rawText,
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception("Failed to upload exam: ${response.body}");
      }
    }
  }

  Future<Map<String, dynamic>> getExamAnalysis(int examId) async {
    final response = await http.get(Uri.parse("$baseUrl/exams/$examId/analysis"), headers: _headers);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to fetch exam analysis for ID $examId");
    }
  }

  Future<Map<String, dynamic>> getStudentProfile() async {
    final response = await http.get(Uri.parse("$baseUrl/students/$currentUserId/profile"), headers: _headers);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to fetch student profile");
    }
  }

  Future<Map<String, dynamic>> submitPracticeAttempt(int practiceId, int questionId, String answer) async {
    final response = await http.post(
      Uri.parse("$baseUrl/practice/$practiceId/submit"),
      headers: _headers,
      body: jsonEncode({
        "question_id": questionId,
        "student_answer": answer
      })
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to submit practice attempt");
    }
  }

  Future<Map<String, dynamic>> generatePracticeSet(int diagnosisId, String concept, int count) async {
    final response = await http.post(
      Uri.parse("$baseUrl/practice/generate"),
      headers: _headers,
      body: jsonEncode({
        "diagnosis_id": diagnosisId,
        "concept": concept,
        "count": count
      })
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to generate practice set");
    }
  }

  Future<Map<String, dynamic>> generateRetest() async {
    final response = await http.post(
      Uri.parse("$baseUrl/retest/generate"),
      headers: _headers
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to generate retest");
    }
  }

  Future<Map<String, dynamic>> submitRetest(int retestId, List<Map<String, dynamic>> answers) async {
    final response = await http.post(
      Uri.parse("$baseUrl/retest/$retestId/submit"),
      headers: _headers,
      body: jsonEncode({"answers": answers})
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to submit retest");
    }
  }

  Future<Map<String, dynamic>> analyzeAttempt({
    required String question,
    required String studentAnswer,
    String? correctAnswer,
    String? workEvidence,
    String? studentId = "student_001",
    String subject = "MATHEMATICS",
  }) async {
    final response = await http.post(
      Uri.parse("$baseUrl/ai/analyze-attempt"),
      headers: _headers,
      body: jsonEncode({
        "student_id": studentId,
        "subject": subject,
        "question": question,
        "correct_answer": correctAnswer,
        "student_answer": studentAnswer,
        "work_evidence": workEvidence ?? "",
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to analyze attempt: ${response.body}");
    }
  }

  Future<Map<String, dynamic>> getModelInfo() async {
    final response = await http.get(Uri.parse("$baseUrl/ai/model-info"), headers: _headers);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to fetch model info");
    }
  }

  Future<Map<String, dynamic>> getProgress() async {
    final response = await http.get(Uri.parse("$baseUrl/progress"), headers: _headers);
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to fetch longitudinal progress");
    }
  }
}
