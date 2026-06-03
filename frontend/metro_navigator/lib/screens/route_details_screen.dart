import 'package:flutter/material.dart';
import 'navigation_screen.dart';

class RouteDetailsScreen extends StatelessWidget {
  const RouteDetailsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final steps = ['Start from selected station', 'Board metro bus', 'Pass 8 stops', 'Arrive at destination'];

    return Scaffold(
      appBar: AppBar(title: const Text('Route Details')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Card(
              child: ListTile(
                title: Text('Best Route'),
                subtitle: Text('Estimated time: 25 minutes\nDistance: 10 km\nTransfer: No transfer required'),
              ),
            ),
            const SizedBox(height: 12),
            ...steps.map((s) => Card(child: ListTile(leading: const Icon(Icons.check_circle), title: Text(s)))),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const NavigationScreen()));
              },
              child: const Text('Start Navigation'),
            ),
          ],
        ),
      ),
    );
  }
}