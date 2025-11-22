#!/usr/bin/env python3
"""
Create Kafka topics for the Steam Analytics project.
Run this after starting the Kafka cluster with docker-compose.
"""

from confluent_kafka.admin import AdminClient, NewTopic
from config.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPICS,
    TOPIC_CONFIGS,
    ANALYTICS_TOPIC_CONFIG,
)
import sys


def create_topics():
    """Create all required Kafka topics."""

    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    # Prepare topic list
    topics_to_create = []

    # Store topics (game-views, wishlist, cart, purchases, searches)
    store_topics = [
        TOPICS["game_views"],
        TOPICS["wishlist_events"],
        TOPICS["cart_events"],
        TOPICS["purchases"],
        TOPICS["searches"],
    ]

    for topic in store_topics:
        topics_to_create.append(
            NewTopic(
                topic,
                num_partitions=TOPIC_CONFIGS["num_partitions"],
                replication_factor=TOPIC_CONFIGS["replication_factor"],
                config=TOPIC_CONFIGS["config"],
            )
        )

    # Analytics topic (different config)
    topics_to_create.append(
        NewTopic(
            TOPICS["analytics"],
            num_partitions=ANALYTICS_TOPIC_CONFIG["num_partitions"],
            replication_factor=ANALYTICS_TOPIC_CONFIG["replication_factor"],
            config=ANALYTICS_TOPIC_CONFIG["config"],
        )
    )

    # Create topics
    print("Creating topics...")
    futures = admin_client.create_topics(topics_to_create)

    # Wait for operations to finish
    for topic, future in futures.items():
        try:
            future.result()  # Block until topic is created
            print(f"Topic '{topic}' created successfully")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Topic '{topic}' already exists")
            else:
                print(f"Failed to create topic '{topic}': {e}")
                sys.exit(1)

    print("\nAll topics ready!")
    print("\nView topics at: http://localhost:8080")


def list_topics():
    """List all existing topics."""

    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    metadata = admin_client.list_topics(timeout=10)

    print("\nExisting topics:")
    for topic in metadata.topics.values():
        print(f"  - {topic.topic} ({len(topic.partitions)} partitions)")


if __name__ == "__main__":
    try:
        create_topics()
        list_topics()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Kafka is running: docker-compose up -d")
        sys.exit(1)
