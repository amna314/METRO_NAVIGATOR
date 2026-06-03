import 'package:flutter/material.dart';
import 'route_details_screen.dart';

class AvailableRoutesScreen extends StatelessWidget {
  final String from;
  final String to;

  const AvailableRoutesScreen({super.key, required this.from, required this.to});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Available Routes')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              leading: const Icon(Icons.directions_bus, color: Color(0xFF004D40)),
              title: Text('$from to $to'),
              subtitle: const Text('Estimated time: 25 minutes\nStops: 8\nTransfer: No transfer'),
              trailing: const Icon(Icons.arrow_forward),
              onTap: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const RouteDetailsScreen()));
              },
            ),
          ),
        ],
      ),
    );
  }
}