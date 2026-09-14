"""
Real-time Stock Data Producer for Kafka
Simulates stock market tick data and publishes to Kafka topic
"""
import json
import time
import random
import logging
import yaml
from datetime import datetime
from kafka import KafkaProducer
from schema import StockTick

# Load configuration
with open('../config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup logging
logging.basicConfig(
    level=getattr(logging, config['logging']['level']),
    format=config['logging']['format'],
    handlers=[
        logging.FileHandler('../logs/producer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('StockProducer')


class StockSimulator:
    """Simulates realistic stock price movements"""
    
    def __init__(self, symbol: str, base_price: float, volatility: float):
        self.symbol = symbol
        self.current_price = base_price
        self.volatility = volatility
        self.previous_prices = []
        
    def generate_tick(self) -> StockTick:
        """Generate a single stock tick"""
        # Random walk with drift
        change = random.gauss(0, self.volatility)
        self.current_price *= (1 + change)
        self.current_price = round(self.current_price, 2)
        
        # Generate volume (higher on bigger moves)
        base_volume = random.randint(1000, 10000)
        volume_multiplier = 1 + abs(change) * 10
        volume = int(base_volume * volume_multiplier)
        
        # Calculate change percent
        if len(self.previous_prices) > 0:
            prev_price = self.previous_prices[-1]
            change_percent = round(((self.current_price - prev_price) / prev_price) * 100, 4)
        else:
            change_percent = 0.0
        
        # Store price history
        self.previous_prices.append(self.current_price)
        if len(self.previous_prices) > 100:
            self.previous_prices.pop(0)
        
        tick = StockTick(
            symbol=self.symbol,
            timestamp=datetime.utcnow().isoformat(),
            price=self.current_price,
            volume=volume,
            change_percent=change_percent
        )
        
        return tick


def main():
    """Main producer loop"""
    logger.info("Starting Stock Data Producer...")
    
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )
    
    topic = config['kafka']['topic']['raw']
    interval = config['producer']['interval_seconds']
    
    # Initialize stock simulators
    simulators = []
    for stock_config in config['producer']['stocks']:
        simulator = StockSimulator(
            symbol=stock_config['symbol'],
            base_price=stock_config['base_price'],
            volatility=stock_config['volatility']
        )
        simulators.append(simulator)
        logger.info(f"Initialized simulator for {stock_config['symbol']}")
    
    logger.info(f"Publishing to topic: {topic}")
    message_count = 0
    
    try:
        while True:
            for simulator in simulators:
                tick = simulator.generate_tick()
                
                # Send to Kafka
                future = producer.send(
                    topic,
                    key=tick.symbol,
                    value=tick.to_dict()
                )
                
                # Wait for confirmation
                record_metadata = future.get(timeout=10)
                message_count += 1
                
                if message_count % 10 == 0:
                    logger.info(
                        f"[{message_count}] Published {tick.symbol}: "
                        f"${tick.price:.2f} ({tick.change_percent:+.2f}%) "
                        f"Vol: {tick.volume}"
                    )
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("Producer stopped by user")
    except Exception as e:
        logger.error(f"Producer error: {e}")
    finally:
        producer.flush()
        producer.close()
        logger.info("Producer closed")


if __name__ == "__main__":
    main()
