class SensorReading {
  final int id;
  final String sensorType;
  final double value;
  final String location;
  final DateTime timestamp;
  final bool isCritical;

  SensorReading({
    required this.id,
    required this.sensorType,
    required this.value,
    required this.location,
    required this.timestamp,
    required this.isCritical,
  });

  factory SensorReading.fromJson(Map<String, dynamic> json) {
    return SensorReading(
      id: json['id'],
      sensorType: json['sensor_type'],
      value: json['value'].toDouble(),
      location: json['location'],
      timestamp: DateTime.parse(json['timestamp']),
      isCritical: json['is_critical'],
    );
  }
}
