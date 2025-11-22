# Kafka Learning Project: Steam-Inspired Analytics Platform

## Project Overview

This is a hands-on Kafka learning project designed to build real-world skills applicable to companies like Valve. The project simulates a Steam-like digital storefront with real-time analytics, combining e-commerce store operations with gaming platform features.

### Learning Goals
- Master core Kafka concepts: producers, consumers, topics, partitions, consumer groups
- Understand real-time stream processing and analytics
- Build foundation for event-driven microservices architecture
- Demonstrate skills relevant to gaming platform infrastructure

### Project Phases
1. **Phase 1 (Current)**: Real-time store analytics - track browsing, wishlists, purchases
2. **Phase 2 (Future)**: Add gameplay tracking - launches, playtime, achievements
3. **Phase 3 (Future)**: Event-driven microservices - order processing, inventory, recommendations

---

## Event Schema Definitions

### 1. GamePageViewed
Tracks when a user views a game's store page.

```json
{
  "eventType": "game_page_viewed",
  "timestamp": "2025-11-21T10:30:45Z",
  "userId": "user_12345",
  "gameId": "game_789",
  "gameName": "Cyberpunk 2077",
  "price": 59.99,
  "onSale": true,
  "salePrice": 29.99,
  "category": "RPG",
  "tags": ["open-world", "story-rich", "cyberpunk"],
  "source": "featured_carousel"
}
```

**Source values**: `featured_carousel`, `search`, `recommendation`, `direct`, `wishlist`, `category_browse`

---

### 2. WishlistAction
Tracks additions/removals from user wishlists.

```json
{
  "eventType": "wishlist_action",
  "timestamp": "2025-11-21T10:31:20Z",
  "userId": "user_12345",
  "gameId": "game_789",
  "action": "added",
  "currentWishlistSize": 15
}
```

**Action values**: `added`, `removed`

---

### 3. CartAction
Tracks items being added/removed from shopping cart.

```json
{
  "eventType": "cart_action",
  "timestamp": "2025-11-21T10:32:10Z",
  "userId": "user_12345",
  "gameId": "game_789",
  "action": "added",
  "currentCartValue": 89.97,
  "itemsInCart": 3
}
```

**Action values**: `added`, `removed`

---

### 4. Purchase
Tracks completed purchases (checkout success).

```json
{
  "eventType": "purchase",
  "timestamp": "2025-11-21T10:35:00Z",
  "userId": "user_12345",
  "orderId": "order_abc123",
  "games": [
    {"gameId": "game_789", "price": 29.99},
    {"gameId": "game_456", "price": 19.99}
  ],
  "totalAmount": 49.98,
  "paymentMethod": "credit_card",
  "region": "US"
}
```

**Payment method values**: `credit_card`, `paypal`, `steam_wallet`, `cryptocurrency`
**Region values**: ISO country codes (`US`, `UK`, `JP`, etc.)

---

### 5. SearchPerformed
Tracks user searches in the store.

```json
{
  "eventType": "search_performed",
  "timestamp": "2025-11-21T10:28:00Z",
  "userId": "user_12345",
  "searchQuery": "open world rpg",
  "resultsCount": 47,
  "filterTags": ["RPG", "open-world"]
}
```

---

## Kafka Topics Architecture

```
store.game-views          # All game page view events
store.wishlist-events     # Wishlist add/remove events
store.cart-events         # Shopping cart modifications
store.purchases           # Completed purchases
store.searches            # Search queries
analytics.metrics         # Processed/aggregated metrics output
```

### Topic Configuration Recommendations
- **Partitions**: Start with 3-6 partitions per topic for parallelism
- **Replication Factor**: 1 for local dev, 3 for production-like setup
- **Retention**: 7 days for raw events, 30 days for analytics

---

## Real-Time Metrics to Calculate

### Sales & Revenue
- **Revenue per minute**: Sum of purchase amounts in rolling 1-minute window
- **Sales velocity**: Number of purchases per minute
- **Average order value**: Total revenue / number of orders
- **Revenue by region**: Breakdown of sales by geographic region

### Conversion Funnel
- **View → Wishlist rate**: % of views that result in wishlist adds
- **Wishlist → Cart rate**: % of wishlisted games added to cart
- **Cart → Purchase rate**: % of cart additions that convert to purchases
- **Overall conversion**: Views → Purchases

### Product Performance
- **Trending games**: Most viewed games in last hour
- **Hot purchases**: Most purchased games in last 15 minutes
- **Wishlist leaders**: Games added to wishlists most frequently
- **Search popularity**: Most common search terms

### User Behavior
- **Cart abandonment rate**: Carts created vs purchases completed
- **Search effectiveness**: % of searches leading to game views within 5 minutes
- **Average session value**: Revenue per active user session
- **Time to purchase**: Average time from first view to purchase

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)

#### Step 1: Environment Setup
- Install Kafka locally or via Docker
- Set up Python development environment
- Create initial project structure

#### Step 2: Event Producer
Build a Python producer that simulates realistic user behavior:
- Generate random users browsing the store
- Simulate realistic user journeys (view → wishlist → cart → purchase)
- Include realistic timing and dropout rates
- Support configurable event generation rates

#### Step 3: Basic Consumer
Create a simple consumer that:
- Reads events from topics
- Prints events to console for verification
- Validates event schema

#### Step 4: Stream Processor
Build a processor that calculates basic metrics:
- Count events by type
- Calculate simple aggregations (total revenue, event counts)
- Output to analytics topic

#### Step 5: Dashboard
Create a simple visualization:
- Real-time metric display (web UI or terminal dashboard)
- Show key metrics updating live
- Display recent events stream

### Phase 2: Advanced Analytics (Week 2)
- Implement windowed aggregations (tumbling/sliding windows)
- Add funnel analysis
- Calculate conversion rates
- Implement trending/hot items detection

### Phase 3: Gameplay Events (Week 3)
- Add game launch events
- Track playtime sessions
- Monitor achievement unlocks
- Correlate gameplay with purchase behavior

---

## Tech Stack

### Required
- **Kafka**: Message broker (latest stable version)
- **Python 3.14+**: Primary language for producers/consumers
- **confluent-kafka-python**: Python Kafka client

### Recommended
- **Docker & Docker Compose**: Easy Kafka setup
- **FastAPI** or **Flask**: Dashboard backend
- **HTML/CSS/JavaScript**: Dashboard frontend (or React for more complex UI)
- **Pandas**: Data manipulation for analytics
- **JSON**: Event serialization format

### Optional/Advanced
- **Kafka Streams** or **ksqlDB**: Advanced stream processing
- **Redis**: Caching for dashboard metrics
- **PostgreSQL**: Persistent storage for aggregated metrics
- **Grafana**: Professional dashboards and monitoring

---

## Sample Game Catalog

For realistic event generation, here's a starter game catalog:

```python
SAMPLE_GAMES = [
    {"gameId": "game_001", "name": "Cyberpunk 2077", "category": "RPG", "price": 59.99, "tags": ["open-world", "story-rich", "cyberpunk"]},
    {"gameId": "game_002", "name": "Elden Ring", "category": "Action", "price": 59.99, "tags": ["souls-like", "open-world", "fantasy"]},
    {"gameId": "game_003", "name": "Stardew Valley", "category": "Simulation", "price": 14.99, "tags": ["farming", "relaxing", "pixel-art"]},
    {"gameId": "game_004", "name": "Counter-Strike 2", "category": "FPS", "price": 0.00, "tags": ["competitive", "multiplayer", "tactical"]},
    {"gameId": "game_005", "name": "Baldur's Gate 3", "category": "RPG", "price": 59.99, "tags": ["story-rich", "party-based", "fantasy"]},
    {"gameId": "game_006", "name": "Hades", "category": "Roguelike", "price": 24.99, "tags": ["action", "roguelike", "mythology"]},
    {"gameId": "game_007", "name": "The Witcher 3", "category": "RPG", "price": 39.99, "tags": ["open-world", "story-rich", "fantasy"]},
    {"gameId": "game_008", "name": "Factorio", "category": "Strategy", "price": 30.00, "tags": ["automation", "building", "management"]},
    {"gameId": "game_009", "name": "Terraria", "category": "Sandbox", "price": 9.99, "tags": ["2D", "crafting", "adventure"]},
    {"gameId": "game_010", "name": "Portal 2", "category": "Puzzle", "price": 19.99, "tags": ["puzzle", "co-op", "comedy"]}
]
```

---

## Realistic User Behavior Patterns

To make the simulation authentic:

### User Journey Patterns
- **Browser**: 70% of users - view 3-5 games, rarely purchase
- **Researcher**: 20% of users - view 5-10 games, add to wishlist, purchase later
- **Buyer**: 10% of users - view 2-3 games, quick purchase decision

### Conversion Rates (Target Realistic Numbers)
- View → Wishlist: ~15%
- Wishlist → Cart: ~25%
- Cart → Purchase: ~60%
- Overall View → Purchase: ~2-3%

### Timing Patterns
- 60% of purchases happen within 24 hours of first view
- Cart abandonment typically happens within 1-2 hours
- Peak activity: evenings and weekends

### Event Distribution
- Game views: 1000 events/minute
- Wishlist actions: 150 events/minute
- Cart actions: 50 events/minute
- Purchases: 30 events/minute
- Searches: 200 events/minute

---

## Success Criteria

You'll know this project is successful when you can:

1. ✅ Generate realistic event streams through Kafka
2. ✅ Process events in real-time with low latency
3. ✅ Calculate accurate conversion funnel metrics
4. ✅ Display live updating dashboard
5. ✅ Explain Kafka concepts clearly (partitions, consumer groups, offset management)
6. ✅ Handle failure scenarios gracefully
7. ✅ Scale event generation up/down without breaking

---

## Next Steps for Implementation

1. **Start with Docker Compose**: Get Kafka + Zookeeper running locally
2. **Build minimal producer**: Generate one event type, publish to one topic
3. **Build minimal consumer**: Read from that topic, print to console
4. **Iterate**: Add more event types, add processing logic, add visualization
5. **Experiment**: Try different partition counts, consumer groups, processing strategies

---

## Future Enhancements (Phase 2+)

- **Gameplay tracking**: Launch events, playtime, achievements
- **Microservices**: Break into order service, inventory service, recommendation engine
- **Advanced analytics**: User segmentation, churn prediction, personalization
- **Monitoring**: Add Prometheus metrics, trace events through system
- **Fault tolerance**: Test consumer rebalancing, handle producer failures
- **Performance**: Benchmark throughput, optimize for high volume

---

## Resources & References

- **Kafka Documentation**: https://kafka.apache.org/documentation/
- **kafka-python docs**: https://kafka-python.readthedocs.io/
- **Confluent tutorials**: https://developer.confluent.io/
- **Steam public stats**: https://store.steampowered.com/stats/ (for realistic numbers)

---

## Notes

- This project prioritizes **learning Kafka fundamentals** over building production-ready code
- Focus on **understanding core concepts** before optimizing for performance
- **Iterate quickly**: Start simple, add complexity gradually
- **Document learnings**: Keep notes on what worked, what didn't, and why
- **Have fun**: Pick games you like for the catalog, make the dashboard engaging!