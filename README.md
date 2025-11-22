# Kafka Analytics Playground

A hands-on Kafka learning project simulating a digital storefront with real-time analytics.

## Quick Start

### 1. Start Kafka Cluster
```bash
docker-compose up -d
```

This starts:
- **Kafka** on `localhost:9092`
- **Zookeeper** on `localhost:2181`
- **Kafka UI** on `http://localhost:8080` (visual interface for topics/messages)

### 2. Verify Kafka is Running
```bash
docker-compose ps
```

All three services should show "Up".

### 3. View Kafka UI
Open browser to: http://localhost:8080

You'll see the Kafka cluster with no topics yet (we'll create them next).

### 4. Stop Kafka Cluster
```bash
docker-compose down
```

To remove all data (start fresh):
```bash
docker-compose down -v
```

## Project Structure

```
kafka-playground/
├── docker-compose.yml          # Kafka + Zookeeper + UI
├── requirements.txt            # Python dependencies
├── config/
│   └── kafka_config.py         # Kafka connection settings
├── producers/
│   ├── event_generator.py      # Main event producer
│   ├── event_schemas.py        # Event data classes
│   └── rate_controller.py      # Time-of-day traffic patterns
├── consumers/
│   ├── analytics_processor.py  # Stream processor
│   └── metrics_calculator.py   # Metric calculations
├── dashboard/
│   ├── app.py                  # FastAPI server
│   ├── static/
│   │   ├── index.html          # Dashboard UI
│   │   ├── style.css
│   │   └── dashboard.js        # Real-time updates via SSE
│   └── metrics_store.py        # In-memory metrics
├── data/
│   └── game_catalog.py         # Sample game data
└── scripts/
    └── setup_topics.sh         # Create Kafka topics
```

## Event Types

1. **game_page_viewed** - User views a game
2. **wishlist_action** - Add/remove from wishlist
3. **cart_action** - Add/remove from cart
4. **purchase** - Completed purchase
5. **search_performed** - User searches store

## Kafka Topics

- `store.game-views` - Game page view events
- `store.wishlist-events` - Wishlist actions
- `store.cart-events` - Cart modifications
- `store.purchases` - Purchase completions
- `store.searches` - Search queries
- `analytics.metrics` - Aggregated metrics output

## Real-Time Metrics

- Revenue per minute
- Events per minute by type
- Conversion funnel (view → wishlist → cart → purchase)
- Trending games (most viewed/purchased)
- Cart abandonment rate
- Search effectiveness

## Development Workflow

1. **Start Kafka**: `docker-compose up -d`
2. **Create topics**: `./scripts/setup_topics.sh`
3. **Run producer**: `python producers/event_generator.py`
4. **Run consumer**: `python consumers/analytics_processor.py`
5. **Start dashboard**: `python dashboard/app.py`
6. **View dashboard**: Open `http://localhost:8000`

## Learning Goals

- Kafka producers, consumers, topics, partitions
- Consumer groups and offset management
- Real-time stream processing with windowing
- Event-driven architecture patterns
- Monitoring and observability

## Phase Roadmap

- **Phase 1 (Current)**: Store analytics with 5 event types
- **Phase 2 (Future)**: Gameplay tracking (launches, playtime, achievements)
- **Phase 3 (Future)**: Microservices architecture (orders, inventory, recommendations)

## Resources

- Full project spec: See `kafka-steam-project.md`
- Kafka docs: https://kafka.apache.org/documentation/
- confluent-kafka-python: https://docs.confluent.io/kafka-clients/python/current/overview.html
