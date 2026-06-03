import 'package:flutter_test/flutter_test.dart';
import 'package:metro_navigator/main.dart';

void main() {
  testWidgets('App loads smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const MetroNavigatorApp());

    expect(find.text('AI Powered\nMetro Bus Navigator'), findsOneWidget);
  });
}