# Design Patterns & Guidelines

## Architecture Patterns

### Event-Driven Architecture
- **Event Sourcing**: All state changes captured as events
- **Stream Processing**: Events flow through Kafka topics
- **Consumer Groups**: Parallel processing with load balancing
- **Topic Partitioning**: 3 partitions for store events, 1 for analytics

### Kafka Patterns

#### Producer Pattern
```python
class EventProducer:
    def __init__(self):
        self.producer = Producer(PRODUCER_CONFIG)
        
    def send_event(self, topic, event):
        self.producer.produce(
            topic,
            key=event.key,
            value=json.dumps(event.dict()),
            callback=self.delivery_callback
        )
        self.producer.poll(0)  # Non-blocking callback processing
```

#### At-Least-Once Delivery
- Producer: `"acks": "all"` with retries
- Consumer: `"enable.auto.commit": False` with manual commits
- Idempotent consumers required for exactly-once semantics

#### Error Handling
- Delivery callbacks track success/failure
- Error counters for monitoring
- Graceful degradation on failures

## Data Modeling

### Event Schema Pattern
All events use Pydantic models with:
- `timestamp`: ISO 8601 datetime
- `event_id`: Unique identifier (UUID)
- `user_id`: User performing action
- Event-specific fields

Example:
```python
class GamePageViewedEvent(BaseModel):
    timestamp: str
    event_id: str
    user_id: str
    game_id: str
    game_title: str
```

### Topic Organization
- **Domain Prefix**: `store.*` for source events, `analytics.*` for derived data
- **Singular/Plural**: Use plural for event streams (`purchases`, `searches`)
- **Hyphenated Names**: `game-views`, `wishlist-events`

## Configuration Management

### Centralized Config
- Single source of truth: `config/kafka_config.py`
- Separate configs for producer/consumer
- Environment-specific settings via constants
- Typed dictionaries for IDE support

### Topic Configuration
- Different configs for different topic types
- Store topics: 3 partitions, 7-day retention
- Analytics topics: 1 partition, 30-day retention
- Snappy compression for efficiency

## Testing Patterns (Future)
- Unit tests for event generation logic
- Integration tests with testcontainers-kafka
- Consumer tests with mock Kafka messages
- End-to-end tests with full pipeline

## Monitoring & Observability
- Kafka UI for visual monitoring (http://localhost:8080)
- Producer delivery callbacks for error tracking
- Event counters in producers/consumers
- Future: Metrics export to analytics topic
