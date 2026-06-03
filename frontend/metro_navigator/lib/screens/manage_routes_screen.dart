import 'package:flutter/material.dart';

class ManageRoutesScreen extends StatelessWidget {
  const ManageRoutesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Routes')),
      body: const Center(child: Text('Admin can add, edit and delete routes here.')),
    );
  }
}