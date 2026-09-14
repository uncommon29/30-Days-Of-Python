# Real-time Kafka Pipeline

A real-time data streaming pipeline using Apache Kafka to process stock market data (simulated).

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Producer  │───▶│    Kafka    │───▶│   Consumer  │───▶│   Output    │
│  (Simulator)│    │   Broker    │    │ (Processor) │    │ (Dashboard) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Features

- **Real-time Data Generation**: Simulates stock market tick data
- **Kafka Streaming**: Uses Kafka topics for message queuing
- **Stream Processing**: Real-time aggregation and anomaly detection
- **Output**: Processed data to console/file with alerts

## Prerequisites

- Python 3.8+
- Apache Kafka (use Docker Compose included)
- Required Python packages (see requirements.txt)

## Quick Start

### 1. Start Kafka with Docker Compose

```bash
docker-compose up -d
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Pipeline

Terminal 1 - Start Producer:
```bash
python src/producer.py
```

Terminal 2 - Start Consumer:
```bash
python src/consumer.py
```

## Project Structure

```
realtime_kafka_pipeline/
├── docker-compose.yml      # Kafka & Zookeeper setup
├── requirements.txt        # Python dependencies
├── config/
│   └── settings.yaml       # Configuration file
├── src/
│   ├── producer.py         # Data producer (stock simulator)
│   ├── consumer.py         # Data consumer (processor)
│   └── schema.py           # Data schemas
├── logs/                   # Log files
└── README.md
```

## Dataset

Simulated stock market data including:
- Stock symbol
- Timestamp
- Current price
- Volume
- Price change percentage

## Configuration

Edit `config/settings.yaml` to customize:
- Kafka bootstrap servers
- Topic names
- Processing parameters
- Alert thresholds

## Monitoring

Check logs in the `logs/` directory:
- `producer.log` - Producer activity
- `consumer.log` - Consumer processing & alerts
