import 'package:flutter/material.dart';
import 'available_routes_screen.dart';

class DestinationSearchScreen extends StatelessWidget {
  const DestinationSearchScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final destinations = [
      'Saddar',
      'Faiz Ahmed Faiz',
      'IIUI',
      'Committee Chowk',
      '6th Road',
      'PIMS',
      'Secretariat',
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Popular Destinations')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: destinations.length,
        itemBuilder: (context, index) {
          final destination = destinations[index];

          return Card(
            child: ListTile(
              leading: const Icon(Icons.location_on, color: Color(0xFF004D40)),
              title: Text(destination),
              subtitle: const Text('Tap to search route'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => AvailableRoutesScreen(
                      from: 'Current Location',
                      to: destination,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}