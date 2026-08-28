import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mindtrace_mobile/screens/home_screen.dart';

void main() {
  testWidgets('MindTrace home screen rendering test', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: HomeScreen()));
    await tester.pumpAndSettle();

    expect(find.text('Analyze Exam'), findsOneWidget);
    expect(find.text('Practice Weak Areas'), findsOneWidget);
  });
}
