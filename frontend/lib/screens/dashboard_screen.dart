import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/sensor_reading.dart';
import '../services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  List<SensorReading> _readings = [];
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchReadings();
  }

  Future<void> _fetchReadings() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final readings = await _apiService.getReadings();
      setState(() {
        _readings = readings;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MEP Infrastructure Hub'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isLoading ? null : _fetchReadings,
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              'Error: $_errorMessage',
              style: const TextStyle(color: Colors.red),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _fetchReadings,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_readings.isEmpty) {
      return const Center(child: Text('No readings available'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _readings.length,
      itemBuilder: (context, index) {
        return _buildReadingCard(_readings[index]);
      },
    );
  }

  Widget _buildReadingCard(SensorReading reading) {
    final dateFormat = DateFormat('MMM dd, yyyy HH:mm:ss');

    return Card(
      color: reading.isCritical ? Colors.red.shade50 : null,
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(
          reading.sensorType == 'Thermal' ? Icons.thermostat : Icons.vibration,
          color: reading.isCritical ? Colors.red : Colors.blue,
          size: 32,
        ),
        title: Row(
          children: [
            Text(
              reading.sensorType,
              style: TextStyle(
                fontWeight:
                    reading.isCritical ? FontWeight.bold : FontWeight.normal,
              ),
            ),
            if (reading.isCritical) ...[
              const SizedBox(width: 8),
              const Icon(Icons.warning, color: Colors.red, size: 20),
            ],
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
                'Value: ${reading.value} ${reading.sensorType == 'Thermal' ? '°C' : 'Hz'}'),
            Text('Location: ${reading.location}'),
            Text('Time: ${dateFormat.format(reading.timestamp)}'),
          ],
        ),
        isThreeLine: true,
      ),
    );
  }
}
