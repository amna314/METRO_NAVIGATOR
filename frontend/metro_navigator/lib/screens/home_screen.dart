import 'package:flutter/material.dart';
import 'route_search_screen.dart';
import 'history_screen.dart';
import 'notifications_screen.dart';
import 'feedback_screen.dart';
import 'profile_screen.dart';
import 'language_screen.dart';
import 'ai_assistant_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final items = [
      _HomeItem('Search Route', Icons.route, const RouteSearchScreen()),
      _HomeItem('AI Assistant', Icons.smart_toy, const AiAssistantScreen()),
      _HomeItem('History', Icons.history, const HistoryScreen()),
      _HomeItem('Notifications', Icons.notifications, const NotificationsScreen()),
      _HomeItem('Feedback', Icons.feedback, const FeedbackScreen()),
      _HomeItem('Language', Icons.language, const LanguageScreen()),
      _HomeItem('Profile', Icons.person, const ProfileScreen()),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Metro Navigator')),
      body: Padding(
        padding: const EdgeInsets.all(18),
        child: GridView.builder(
          itemCount: items.length,
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
          ),
          itemBuilder: (context, index) {
            final item = items[index];

            return InkWell(
              borderRadius: BorderRadius.circular(22),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => item.screen),
                );
              },
              child: Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(22),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(item.icon, size: 42, color: const Color(0xFF00A884)),
                    const SizedBox(height: 12),
                    Text(
                      item.title,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _HomeItem {
  final String title;
  final IconData icon;
  final Widget screen;

  _HomeItem(this.title, this.icon, this.screen);
}