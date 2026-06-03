import 'package:flutter/material.dart';
import 'available_routes_screen.dart';

class RouteSearchScreen extends StatefulWidget {
  const RouteSearchScreen({super.key});

  @override
  State<RouteSearchScreen> createState() => _RouteSearchScreenState();
}

class _RouteSearchScreenState extends State<RouteSearchScreen> {
  final fromController = TextEditingController(text: 'Current Location');
  final toController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            color: const Color(0xFFEAF4EF),
            child: const Center(
              child: Icon(
                Icons.map,
                size: 180,
                color: Color(0x33004D40),
              ),
            ),
          ),
          Positioned(
            top: 45,
            right: 24,
            child: CircleAvatar(
              radius: 32,
              backgroundColor: Colors.white,
              child: IconButton(
                icon: const Icon(Icons.menu, color: Color(0xFF004D40)),
                onPressed: () {},
              ),
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              padding: const EdgeInsets.fromLTRB(24, 18, 24, 28),
              decoration: const BoxDecoration(
                color: Color(0xFFFAF7F0),
                borderRadius: BorderRadius.vertical(top: Radius.circular(34)),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Center(
                    child: Container(
                      width: 55,
                      height: 5,
                      decoration: BoxDecoration(
                        color: Colors.black12,
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                  ),
                  const SizedBox(height: 32),
                  const Text(
                    'Where to?',
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Find the best route for your journey',
                    style: TextStyle(fontSize: 17, color: Colors.grey),
                  ),
                  const SizedBox(height: 24),
                  Container(
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(22),
                      border: Border.all(color: Colors.black12),
                    ),
                    child: Column(
                      children: [
                        _RouteField(
                          dotColor: const Color(0xFFFF4B5C),
                          label: 'FROM',
                          controller: fromController,
                        ),
                        const Divider(height: 28),
                        _RouteField(
                          dotColor: Colors.black87,
                          label: 'TO',
                          controller: toController,
                          hint: 'Where are you going?',
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    height: 62,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF004D40),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(18),
                        ),
                      ),
                      icon: const Icon(Icons.search, size: 30),
                      label: const Text(
                        'Search routes',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => AvailableRoutesScreen(
                              from: fromController.text,
                              to: toController.text.isEmpty
                                  ? 'Destination'
                                  : toController.text,
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _RouteField extends StatelessWidget {
  final Color dotColor;
  final String label;
  final String? hint;
  final TextEditingController controller;

  const _RouteField({
    required this.dotColor,
    required this.label,
    required this.controller,
    this.hint,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(radius: 7, backgroundColor: dotColor),
        const SizedBox(width: 22),
        Expanded(
          child: TextField(
            controller: controller,
            decoration: InputDecoration(
              labelText: label,
              hintText: hint,
              border: InputBorder.none,
            ),
            style: const TextStyle(fontSize: 22),
          ),
        ),
      ],
    );
  }
}