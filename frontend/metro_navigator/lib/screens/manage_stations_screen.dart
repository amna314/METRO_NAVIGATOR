import 'package:flutter/material.dart';

class ManageStationsScreen extends StatelessWidget {
  const ManageStationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Stations')),
      body: const Center(child: Text('Admin can add, edit and delete stations here.')),
    );
  }
}