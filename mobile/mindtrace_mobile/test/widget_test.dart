import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mindtrace_mobile/main.dart';

void main() {
  testWidgets('MindTrace app renders home screen correctly', (WidgetTester tester) async {
    await tester.pumpWidget(const MindTraceApp());
    await tester.pumpAndSettle();

    expect(find.text('MindTrace'), findsOneWidget);
    expect(find.text('Analyze Exam'), findsOneWidget);
    expect(find.text('Practice Weak Areas'), findsOneWidget);
  });
}
