"""
Real-time Stock Data Consumer for Kafka
Processes streaming stock data with anomaly detection and aggregations
"""
import json
import time
import logging
import yaml
import uuid
from datetime import datetime, timedelta
from collections import deque
from kafka import KafkaConsumer, KafkaProducer
from schema import StockTick, ProcessedTick, Alert

# Load configuration
with open('../config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup logging
logging.basicConfig(
    level=getattr(logging, config['logging']['level']),
    format=config['logging']['format'],
    handlers=[
        logging.FileHandler('../logs/consumer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('StockConsumer')


class StreamProcessor:
    """Processes streaming stock data with windowed aggregations"""
    
    def __init__(self, symbol: str, window_size: int = 10):
        self.symbol = symbol
        self.window_size = window_size
        self.price_window = deque(maxlen=window_size)
        self.volume_window = deque(maxlen=window_size)
        self.last_price = None
        
    def process_tick(self, tick: StockTick, threshold: float) -> tuple[ProcessedTick, Alert | None]:
        """Process a single tick and return processed data + optional alert"""
        
        # Update windows
        self.price_window.append(tick.price)
        self.volume_window.append(tick.volume)
        
        # Calculate moving averages
        ma_5 = None
        ma_10 = None
        
        if len(self.price_window) >= 5:
            ma_5 = round(sum(list(self.price_window)[-5:]) / 5, 2)
        
        if len(self.price_window) >= 10:
            ma_10 = round(sum(self.price_window) / 10, 2)
        
        # Anomaly detection
        is_anomaly = False
        anomaly_reason = None
        alert = None
        
        # Check for significant price change
        if self.last_price and abs(tick.change_percent) > threshold * 100:
            is_anomaly = True
            anomaly_reason = f"Price change {tick.change_percent:+.2f}% exceeds threshold"
            
            # Create alert
            alert = Alert(
                alert_id=str(uuid.uuid4())[:8],
                symbol=tick.symbol,
                timestamp=datetime.utcnow().isoformat(),
                alert_type="PRICE_ANOMALY",
                severity="HIGH" if abs(tick.change_percent) > 10 else "MEDIUM",
                message=f"{tick.symbol} {anomaly_reason}",
                current_price=tick.price,
                threshold_exceeded=threshold
            )
        
        # Check for volume spike
        if len(self.volume_window) >= 5:
            avg_volume = sum(list(self.volume_window)[:-1]) / (len(self.volume_window) - 1)
            if tick.volume > avg_volume * 3:
                is_anomaly = True
                anomaly_reason = f"Volume spike: {tick.volume} vs avg {avg_volume:.0f}"
                
                if not alert:
                    alert = Alert(
                        alert_id=str(uuid.uuid4())[:8],
                        symbol=tick.symbol,
                        timestamp=datetime.utcnow().isoformat(),
                        alert_type="VOLUME_SPIKE",
                        severity="LOW",
                        message=f"{tick.symbol} {anomaly_reason}",
                        current_price=tick.price,
                        threshold_exceeded=3.0
                    )
        
        self.last_price = tick.price
        
        # Create processed tick
        processed = ProcessedTick(
            symbol=tick.symbol,
            timestamp=tick.timestamp,
            price=tick.price,
            volume=tick.volume,
            change_percent=tick.change_percent,
            moving_avg_5=ma_5,
            moving_avg_10=ma_10,
            is_anomaly=is_anomaly,
            anomaly_reason=anomaly_reason
        )
        
        return processed, alert


def main():
    """Main consumer loop"""
    logger.info("Starting Stock Data Consumer...")
    
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        config['kafka']['topic']['raw'],
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        group_id=config['consumer']['group_id'],
        auto_offset_reset=config['consumer']['auto_offset_reset'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None
    )
    
    # Initialize Kafka producer for processed data
    producer = KafkaProducer(
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )
    
    processed_topic = config['kafka']['topic']['processed']
    alerts_topic = config['kafka']['topic']['alerts']
    threshold = config['consumer']['processing']['anomaly_threshold']
    window_size = config['consumer']['processing']['window_size_seconds']
    
    # Initialize processors for each stock
    processors = {}
    
    logger.info(f"Subscribed to topic: {config['kafka']['topic']['raw']}")
    logger.info(f"Anomaly threshold: {threshold * 100}%")
    
    message_count = 0
    alert_count = 0
    
    try:
        for message in consumer:
            try:
                tick_data = message.value
                tick = StockTick.from_dict(tick_data)
                
                # Get or create processor for this stock
                if tick.symbol not in processors:
                    processors[tick.symbol] = StreamProcessor(
                        symbol=tick.symbol,
                        window_size=window_size
                    )
                    logger.info(f"Created processor for {tick.symbol}")
                
                # Process the tick
                processor = processors[tick.symbol]
                processed, alert = processor.process_tick(tick, threshold)
                
                # Send processed data to Kafka
                producer.send(
                    processed_topic,
                    key=processed.symbol,
                    value=processed.to_dict()
                )
                
                message_count += 1
                
                # Send alert if detected
                if alert:
                    producer.send(
                        alerts_topic,
                        key=alert.symbol,
                        value=alert.to_dict()
                    )
                    alert_count += 1
                    
                    logger.warning(
                        f"🚨 ALERT [{alert.alert_id}] {alert.message} | "
                        f"Price: ${alert.current_price:.2f} | Severity: {alert.severity}"
                    )
                
                # Log summary every 20 messages
                if message_count % 20 == 0:
                    logger.info(
                        f"[{message_count}] Processed | "
                        f"{tick.symbol}: ${tick.price:.2f} | "
                        f"MA5: ${processed.moving_avg_5 if processed.moving_avg_5 else 'N/A'} | "
                        f"Anomaly: {'⚠️' if processed.is_anomaly else '✓'}"
                    )
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Consumer error: {e}")
    finally:
        producer.flush()
        producer.close()
        consumer.close()
        logger.info(f"Consumer closed. Total processed: {message_count}, Alerts: {alert_count}")


if __name__ == "__main__":
    main()
