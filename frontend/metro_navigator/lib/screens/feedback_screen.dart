import 'package:flutter/material.dart';

class FeedbackScreen extends StatelessWidget {
  const FeedbackScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Feedback')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const TextField(maxLines: 5, decoration: InputDecoration(labelText: 'Write feedback', border: OutlineInputBorder())),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: () {}, child: const Text('Submit Feedback')),
          ],
        ),
      ),
    );
  }
}