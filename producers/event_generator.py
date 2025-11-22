"""
Event producer for Steam Analytics simulation.
Generates realistic game page view events and sends them to Kafka.
"""

import json
import time
import random
from typing import Dict, Any
from confluent_kafka import Producer
from config.kafka_config import PRODUCER_CONFIG, TOPICS
from producers.event_schemas import GamePageViewedEvent
from data.game_catalog import get_weighted_game_choices, get_purchase_source


class EventProducer:
    """Kafka producer for generating and sending events."""

    def __init__(self):
        """Initialize the Kafka producer."""
        self.producer = Producer(PRODUCER_CONFIG)
        self.events_sent = 0
        self.errors = 0

    def delivery_callback(self, err, msg):
        """
        Callback for message delivery reports.
        Called once for each message produced to indicate delivery result.
        """
        if err is not None:
            self.errors += 1
            print(f"Message delivery failed: {err}")
        else:
            self.events_sent += 1
            if self.events_sent % 100 == 0:  # Log every 100 messages
                print(
                    f"{self.events_sent} events sent | "
                    f"Topic: {msg.topic()} | "
                    f"Partition: {msg.partition()} | "
                    f"Offset: {msg.offset()}"
                )

    def send_event(self, topic: str, event: Dict[str, Any], key: str = None):
        """
        Send an event to a Kafka topic.

        Args:
            topic: Kafka topic name
            event: Event dictionary to send
            key: Optional partition key (uses userId by default)
        """
        try:
            # Use userId as partition key for even distribution
            partition_key = key or event.get("userId", "")

            # Serialize to JSON
            event_json = json.dumps(event)

            # Send to Kafka (async)
            self.producer.produce(
                topic=topic,
                value=event_json.encode("utf-8"),
                key=partition_key.encode("utf-8"),
                callback=self.delivery_callback,
            )

            # Trigger delivery report callbacks from previous produce() calls
            self.producer.poll(0)

        except Exception as e:
            print(f"Error sending event: {e}")
            self.errors += 1

    def generate_game_view_event(self) -> GamePageViewedEvent:
        """
        Generate a realistic game page view event.

        TODO(human): Implement this function to create realistic game view events.

        input:

        Requirements:
        - Select a game from GAME_CATALOG (use weighted random selection based on popularity)
        - Generate a random userId (format: "user_<random_number>")
        - Choose a realistic source (featured_carousel=40%, search=25%, recommendation=20%,
          category_browse=10%, direct=5%)
        - Randomly decide if game is on sale (20% chance)
        - If on sale, set salePrice to 70-90% of original price
        - Return a GamePageViewedEvent with all required fields

        Hints:
        - Use random.choices() with weights for game selection
        - Use random.randint() for userId generation
        - Use random.random() < probability for boolean decisions
        - GamePageViewedEvent will auto-generate timestamp

        Returns:
            GamePageViewedEvent: A validated event ready to send
        """

        games, weights = get_weighted_game_choices()
        game = random.choices(games, weights=weights)[0]
        userId = f"user_{random.randint(1000, 9999)}"
        source = get_purchase_source()
        onSale = random.random() < 0.2
        salePrice = game["price"] * random.uniform(0.7, 0.9) if onSale else None
        category = game["category"]
        tags = game["tags"]

        return GamePageViewedEvent(userId=userId, gameId=game["gameId"], gameName=game["name"], price=game["price"], onSale=onSale, salePrice=salePrice, category=category, tags=tags, source=source)

    def run(self, events_per_second: int = 10, duration_seconds: int = 60):
        """
        Run the event generator for a specified duration.

        Args:
            events_per_second: Rate of event generation
            duration_seconds: How long to run (None = run forever)
        """
        print("Starting event producer...")
        print(f"Rate: {events_per_second} events/second")
        print(f"Duration: {duration_seconds}s" if duration_seconds else "⏱️  Duration: Forever")
        print(f"Target topic: {TOPICS['game_views']}\n")

        start_time = time.time()
        sleep_interval = 1.0 / events_per_second

        try:
            while True:
                # Check if we've reached duration limit
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                # Generate and send event
                event = self.generate_game_view_event()

                if event:  # Only send if event was generated
                    event_dict = event.model_dump()
                    self.send_event(
                        topic=TOPICS["game_views"],
                        event=event_dict,
                        key=event.userId,
                    )

                # Rate limiting
                time.sleep(sleep_interval)

        except KeyboardInterrupt:
            print("\nStopping producer (Ctrl+C pressed)...")

        finally:
            # Flush any remaining messages
            print("\nFlushing remaining messages...")
            self.producer.flush(timeout=10)

            # Print final stats
            elapsed = time.time() - start_time
            print("\nFinal stats:")
            print(f"   • Events sent: {self.events_sent}")
            print(f"   • Errors: {self.errors}")
            print(f"   • Duration: {elapsed:.1f}s")
            print(f"   • Rate: {self.events_sent / elapsed:.1f} events/sec")


if __name__ == "__main__":
    producer = EventProducer()

    # Run for 60 seconds at 10 events/second (600 total events)
    # Change these values to experiment!
    producer.run(events_per_second=10, duration_seconds=60)
