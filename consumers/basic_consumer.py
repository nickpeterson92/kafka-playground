"""
Basic Kafka consumer for viewing game page view events.
Reads from store.game-views topic and displays events in real-time.
"""

import json
from typing import Callable, Dict, Any
from confluent_kafka import Consumer, KafkaError
from config.kafka_config import CONSUMER_CONFIG, TOPICS
from producers.event_schemas import GamePageViewedEvent, WishlistActionEvent, CartActionEvent, PurchaseEvent, SearchPerformedEvent
from pydantic import ValidationError
from data.game_catalog import get_game_by_id


class EventConsumer:
    """Kafka consumer for reading and displaying events."""

    def __init__(self, topics: list[str]):
        """
        Initialize the Kafka consumer.

        Args:
            topics: List of topic names to subscribe to
        """
        self.consumer = Consumer(CONSUMER_CONFIG)
        self.topics = topics
        self.events_consumed = 0
        self.errors = 0

        # Subscribe to topics
        self.consumer.subscribe(self.topics)
        print(f"Subscribed to topics: {', '.join(self.topics)}")
    
    def handle_game_page_viewed_event(self, event_data: GamePageViewedEvent) -> None:
        if event_data.onSale:
            print(f"🔥 SALE! Game {event_data.gameName} viewed by {event_data.userId} for {event_data.salePrice} (discounted from {event_data.price}) from {event_data.source} at {event_data.timestamp}")
        else:
            print(f"🎮 Game {event_data.gameName} viewed by {event_data.userId} for {event_data.price} from {event_data.source} at {event_data.timestamp}")
        
    def handle_wishlist_action_event(self, event_data: WishlistActionEvent) -> None:
        gameName = get_game_by_id(event_data.gameId)["name"] if get_game_by_id(event_data.gameId) else "Unknown Game"
        print(f"🧞 Wishlist action: {event_data.action} for {gameName} by {event_data.userId} at {event_data.timestamp}")

    def handle_cart_action_event(self, event_data: CartActionEvent) -> None:
        gameName = get_game_by_id(event_data.gameId)["name"] if get_game_by_id(event_data.gameId) else "Unknown Game"
        print(f"🛒 Cart action: {event_data.action} for {gameName} by {event_data.userId} at {event_data.timestamp}")

    def handle_purchase_event(self, event_data: PurchaseEvent) -> None:
        print(f"💰 Purchase: {event_data.orderId} by {event_data.userId} at {event_data.timestamp} for {event_data.totalAmount} items: {event_data.games}")

    def handle_search_performed_event(self, event_data: SearchPerformedEvent) -> None:
        print(f"🔍 Search performed: {event_data.searchQuery} by {event_data.userId} at {event_data.timestamp}")
    
    def build_event_handlers(self) -> dict[type, Callable[[Any], None]]:
        return {
            GamePageViewedEvent: self.handle_game_page_viewed_event,
            WishlistActionEvent: self.handle_wishlist_action_event,
            CartActionEvent: self.handle_cart_action_event,
            PurchaseEvent: self.handle_purchase_event,
            SearchPerformedEvent: self.handle_search_performed_event,
        }

    def process_event(self, event_data: Dict[str, Any]) -> None:
        """
        Process and display a single event.
        Converts dict to appropriate Pydantic model and calls handler.

        Args:
            event_data: Dictionary containing the event fields
        """
        # Map eventType to Pydantic model class
        event_type_map = {
            "game_page_viewed": GamePageViewedEvent,
            "wishlist_action": WishlistActionEvent,
            "cart_action": CartActionEvent,
            "purchase": PurchaseEvent,
            "search_performed": SearchPerformedEvent,
        }

        try:
            # Get the event type from the dict
            event_type = event_data.get("eventType")

            if event_type not in event_type_map:
                print(f"⚠️  Unknown event type: {event_type}")
                return

            # Convert dict to Pydantic model (validates data)
            model_class = event_type_map[event_type]
            event_model = model_class(**event_data)

            # Get handlers and call the appropriate one
            event_handlers = self.build_event_handlers()
            handler = event_handlers.get(type(event_model))

            if handler:
                handler(event_model)
            else:
                print(f"No handler for {type(event_model)}")

        except ValidationError as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error in process_event: {e}")

    def run(self, max_events: int = None):
        """
        Run the consumer and process events.

        Args:
            max_events: Maximum number of events to consume (None = run forever)
        """
        print("Starting consumer...")
        print(f"Max events: {max_events if max_events else '∞ (forever)'}\n")

        try:
            while True:
                # Check if we've hit the limit
                if max_events and self.events_consumed >= max_events:
                    print(f"\nReached max events limit ({max_events})")
                    break

                # Poll for messages (timeout 1 second)
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    # No message available within timeout
                    continue

                if msg.error():
                    # Handle errors
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition - not a real error
                        continue
                    else:
                        # Real error
                        self.errors += 1
                        print(f"Consumer error: {msg.error()}")
                        continue

                # Successfully received a message
                try:
                    # Decode and parse JSON
                    event_json = msg.value().decode("utf-8")
                    event_data = json.loads(event_json)

                    # Process and display the event
                    self.process_event(event_data)

                    self.events_consumed += 1

                    # Commit offset after successful processing
                    self.consumer.commit(asynchronous=False)

                except json.JSONDecodeError as e:
                    self.errors += 1
                    print(f"Failed to parse JSON: {e}")
                except Exception as e:
                    self.errors += 1
                    print(f"Error processing event: {e}")

        except KeyboardInterrupt:
            print("\nStopping consumer (Ctrl+C pressed)...")

        finally:
            # Clean shutdown
            print("\nClosing consumer...")
            self.consumer.close()

            # Print final stats
            print("\nFinal Stats:")
            print(f"   • Events consumed: {self.events_consumed}")
            print(f"   • Errors: {self.errors}")


if __name__ == "__main__":
    # Subscribe to all store event topics
    consumer = EventConsumer(topics=[
        TOPICS["game_views"],
        TOPICS["wishlist_events"],
        TOPICS["cart_events"],
        TOPICS["purchases"],
        TOPICS["searches"],
    ])

    # Run forever (or until Ctrl+C)
    # Change max_events to limit: consumer.run(max_events=100)
    consumer.run()
