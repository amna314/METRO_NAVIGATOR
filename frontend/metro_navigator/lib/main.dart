import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';

void main() {
  runApp(const MetroNavigatorApp());
}

class MetroNavigatorApp extends StatelessWidget {
  const MetroNavigatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Metro Navigator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: const Color(0xFFFAF7F0),
        primaryColor: const Color(0xFF004D40),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF004D40),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF004D40),
          foregroundColor: Colors.white,
        ),
      ),
      home: const SplashScreen(),
    );
  }
}