import 'package:flutter/material.dart';

class NavigationScreen extends StatelessWidget {
  const NavigationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Step by Step Navigation')),
      body: const Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            Icon(Icons.map, size: 100, color: Color(0xFF004D40)),
            SizedBox(height: 20),
            Text('Follow the metro route instructions shown here.', style: TextStyle(fontSize: 18)),
            SizedBox(height: 20),
            Card(child: ListTile(title: Text('1. Go to platform'), subtitle: Text('Wait for metro bus'))),
            Card(child: ListTile(title: Text('2. Board the bus'), subtitle: Text('Stay until destination station'))),
            Card(child: ListTile(title: Text('3. Exit station'), subtitle: Text('You have reached your destination'))),
          ],
        ),
      ),
    );
  }
}