import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/sensor_reading.dart';

class ApiService {
  // Change to your machine's IP for mobile testing
  static const String baseUrl = 'http://localhost:8000';

  Future<List<SensorReading>> getReadings() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/readings'));

      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(response.body);
        return data.map((json) => SensorReading.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load readings');
      }
    } catch (e) {
      throw Exception('Backend offline: $e');
    }
  }

  Future<SensorReading> createReading({
    required String sensorType,
    required double value,
    required String location,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/readings'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'sensor_type': sensorType,
          'value': value,
          'location': location,
        }),
      );

      if (response.statusCode == 200) {
        return SensorReading.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to create reading');
      }
    } catch (e) {
      throw Exception('Backend offline: $e');
    }
  }
}
