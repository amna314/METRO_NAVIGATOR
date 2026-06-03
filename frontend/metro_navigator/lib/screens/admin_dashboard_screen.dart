import 'package:flutter/material.dart';
import 'manage_routes_screen.dart';
import 'manage_stations_screen.dart';

class AdminDashboardScreen extends StatelessWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Admin Dashboard')),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.route),
            title: const Text('Manage Routes'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ManageRoutesScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.location_city),
            title: const Text('Manage Stations'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ManageStationsScreen())),
          ),
          const ListTile(leading: Icon(Icons.monitor_heart), title: Text('Monitor System')),
          const ListTile(leading: Icon(Icons.schedule), title: Text('Update Schedules')),
        ],
      ),
    );
  }
}