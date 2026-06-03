import 'package:flutter/material.dart';

class AiAssistantScreen extends StatelessWidget {
  const AiAssistantScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Assistant')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Text('Ask route questions like: How do I go from IIUI to Saddar?'),
            const SizedBox(height: 20),
            const TextField(decoration: InputDecoration(labelText: 'Ask here', border: OutlineInputBorder())),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: () {}, child: const Text('Ask AI')),
          ],
        ),
      ),
    );
  }
}