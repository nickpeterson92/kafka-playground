"""
Kafka configuration settings for producers and consumers.
"""

from typing import Dict, Any


# Kafka broker configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# Producer configuration
PRODUCER_CONFIG: Dict[str, Any] = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "client.id": "steam-analytics-producer",
    "acks": "all",  # Wait for all replicas to acknowledge
    "retries": 3,
    "compression.type": "snappy",  # Compress messages for efficiency
    "linger.ms": 10,  # Batch messages for up to 10ms for better throughput
}

# Consumer configuration
CONSUMER_CONFIG: Dict[str, Any] = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "analytics-processor",
    "client.id": "steam-analytics-consumer",
    "auto.offset.reset": "earliest",  # Start from beginning if no offset exists
    "enable.auto.commit": False,  # Manual offset management for reliability
    "max.poll.interval.ms": 300000,  # 5 minutes
}

# Topic names
TOPICS = {
    "game_views": "store.game-views",
    "wishlist_events": "store.wishlist-events",
    "cart_events": "store.cart-events",
    "purchases": "store.purchases",
    "searches": "store.searches",
    "analytics": "analytics.metrics",
}

# Topic configuration for creation
TOPIC_CONFIGS = {
    "num_partitions": 3,
    "replication_factor": 1,  # Single broker in dev
    "config": {
        "retention.ms": 604800000,  # 7 days
        "compression.type": "snappy",
    },
}

# Analytics topic has different config (fewer partitions, longer retention)
ANALYTICS_TOPIC_CONFIG = {
    "num_partitions": 1,
    "replication_factor": 1,
    "config": {
        "retention.ms": 2592000000,  # 30 days
        "compression.type": "snappy",
    },
}
