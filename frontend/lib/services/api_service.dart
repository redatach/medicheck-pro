import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  static final String _baseUrl = dotenv.get('API_URL', 
      fallback: 'http://127.0.0.1:8000/api');
  
  static Future<Map<String, dynamic>> analyzeSymptoms({
    required String description,
    int? age,
    String? gender,
    String? imageBase64,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/diagnostic/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'description': description,
          'age': age,
          'gender': gender,
          'image': imageBase64,
        }),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {
          'error': 'Erreur API: ${response.statusCode}',
          'analysis': {
            'urgency_level': 'medium',
            'recommendations': 'Consultez un médecin pour un diagnostic précis.',
          }
        };
      }
    } catch (e) {
      return {
        'error': 'Erreur de connexion: $e',
        'analysis': {
          'urgency_level': 'low',
          'recommendations': 'Veuillez vérifier votre connexion internet.',
        }
      };
    }
  }
  
  static Future<Map<String, dynamic>> sendChatMessage(
    String message, 
    String? conversationId
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/chat/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'message': message,
          'conversation_id': conversationId,
        }),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Erreur chat: $e');
    }
    
    // Fallback pour développement
    return {
      'response': 'Je suis votre assistant médical. Décrivez vos symptômes en détail.',
      'conversation_id': 'temp_123',
    };
  }
  
  static Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/health/'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Erreur health check: $e');
    }
    
    return {'status': 'unavailable', 'service': 'MediCheck API'};
  }
}
