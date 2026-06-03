import 'package:flutter/material.dart';

class LanguageScreen extends StatelessWidget {
  const LanguageScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Select Language')),
      body: ListView(
        children: const [
          ListTile(leading: Icon(Icons.language), title: Text('English')),
          ListTile(leading: Icon(Icons.language), title: Text('Urdu')),
        ],
      ),
    );
  }
}