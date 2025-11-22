# Codebase Structure

## Directory Overview

```
kafka-playground/
├── config/                 # Kafka configuration
├── producers/              # Event generation
├── consumers/              # Stream processing
├── dashboard/              # FastAPI web UI
├── data/                   # Static data (game catalog)
├── scripts/                # Admin utilities
├── .kafka/                 # Kafka local data
├── .serena/                # Serena project metadata
├── docker-compose.yml      # Kafka cluster definition
└── requirements.txt        # Python dependencies
```

## Key Modules

### config/
- `kafka_config.py`: Centralized Kafka settings
  - `KAFKA_BOOTSTRAP_SERVERS`: Broker address
  - `PRODUCER_CONFIG`: Producer settings (acks, retries, compression)
  - `CONSUMER_CONFIG`: Consumer settings (group.id, offset management)
  - `TOPICS`: Topic name mappings
  - `TOPIC_CONFIGS`: Topic creation parameters

### producers/
- `event_generator.py`: Main producer with `EventProducer` class
  - Methods: `send_event`, `generate_game_view_event`, `run`
  - Handles delivery callbacks and error tracking
- `event_schemas.py`: Pydantic event models
  - `GamePageViewedEvent`, `WishlistActionEvent`, `CartActionEvent`
  - `PurchaseEvent`, `SearchPerformedEvent`, `PurchaseItem`
- `multi_event_generator.py`: Enhanced generator (implementation TBD)

### consumers/
- `basic_consumer.py`: Basic consumer implementation

### data/
- `game_catalog.py`: Sample game data for event generation

### scripts/
- `setup_topics.py`: Topic creation utility
  - Functions: `create_topics()`, `list_topics()`
  - Uses AdminClient from confluent_kafka.admin

### dashboard/
- Directory exists but implementation pending
- Planned: FastAPI app with SSE for real-time metrics

## Kafka Topics Structure

**Store Events** (3 partitions, 7-day retention):
- `store.game-views`
- `store.wishlist-events`
- `store.cart-events`
- `store.purchases`
- `store.searches`

**Analytics Output** (1 partition, 30-day retention):
- `analytics.metrics`

## Event Flow
```
Event Generator → Kafka Topics → Analytics Consumer → Metrics Topic → Dashboard
```
