"""
Multi-event producer for Steam Analytics simulation.
Generates all 5 event types with realistic distributions.
"""

import json
import time
import random
from typing import Dict, Any
from confluent_kafka import Producer
from config.kafka_config import PRODUCER_CONFIG, TOPICS
from producers.event_schemas import (
    GamePageViewedEvent,
    WishlistActionEvent,
    CartActionEvent,
    PurchaseItem,
    PurchaseEvent,
    SearchPerformedEvent,
)
from data.game_catalog import get_weighted_game_choices, get_purchase_source, CATEGORIES, SEARCH_QUERIES
from pydantic import BaseModel


class MultiEventProducer:
    """Kafka producer for generating multiple event types."""

    # Event type distribution (probabilities sum to 1.0)
    # Based on realistic conversion funnel metrics
    EVENT_WEIGHTS = {
        "game_page_viewed": 0.67,  # 67% - Most common event
        "search_performed": 0.13,  # 13% - Users searching
        "wishlist_action": 0.10,   # 10% - Wishlist adds/removes
        "cart_action": 0.08,       # 8% - Cart modifications
        "purchase": 0.02,          # 2% - Actual purchases (rare!)
    }

    EVENT_TYPE_TO_TOPIC = {
      "game_page_viewed": "store.game-views",
      "wishlist_action": "store.wishlist-events",
      "cart_action": "store.cart-events",
      "purchase": "store.purchases",
      "search_performed": "store.searches",
    }

    def __init__(self):
        """Initialize the Kafka producer."""
        self.producer = Producer(PRODUCER_CONFIG)
        self.events_sent = 0
        self.errors = 0
        self.event_counts = {event_type: 0 for event_type in self.EVENT_WEIGHTS.keys()}

    def delivery_callback(self, err, msg):
        """Callback for message delivery reports."""
        if err is not None:
            self.errors += 1
            print(f"❌ Message delivery failed: {err}")
        else:
            self.events_sent += 1
            if self.events_sent % 100 == 0:
                print(
                    f"✅ {self.events_sent} events sent | "
                    f"Views: {self.event_counts['game_page_viewed']} | "
                    f"Wishlist: {self.event_counts['wishlist_action']} | "
                    f"Cart: {self.event_counts['cart_action']} | "
                    f"Purchase: {self.event_counts['purchase']} | "
                    f"Search: {self.event_counts['search_performed']}"
                )

    def send_event(self, topic: str, event: Dict[str, Any], key: str = None):
        """Send an event to a Kafka topic."""
        try:
            partition_key = key or event.get("userId", "")
            event_json = json.dumps(event)

            self.producer.produce(
                topic=topic,
                value=event_json.encode("utf-8"),
                key=partition_key.encode("utf-8"),
                callback=self.delivery_callback,
            )

            self.producer.poll(0)

        except Exception as e:
            print(f"❌ Error sending event: {e}")
            self.errors += 1

    def generate_game_view_event(self) -> GamePageViewedEvent:
        """Generate a game page view event (already implemented)."""
        games, weights = get_weighted_game_choices()
        game = random.choices(games, weights=weights)[0]
        userId = f"user_{random.randint(1000, 9999)}"
        source = get_purchase_source()
        onSale = random.random() < 0.2
        salePrice = game["price"] * random.uniform(0.7, 0.9) if onSale else None

        return GamePageViewedEvent(
            userId=userId,
            gameId=game["gameId"],
            gameName=game["name"],
            price=game["price"],
            onSale=onSale,
            salePrice=salePrice,
            category=game["category"],
            tags=game["tags"],
            source=source,
        )

    def generate_wishlist_action_event(self) -> WishlistActionEvent:
        """
        Generate a wishlist action event (add or remove).

        TODO(human): Implement this function.

        Requirements:
        - Generate random userId (same format as game views)
        - Select random game from catalog
        - 80% "added", 20% "removed" (more adds than removes)
        - Generate realistic currentWishlistSize (1-50 range)
          - If action is "added", size should be 1-50
          - If action is "removed", size should be 0-49 (can't remove from empty)

        Hints:
        - Use random.choice(["added", "removed"]) with weights
        - Or: action = "added" if random.random() < 0.8 else "removed"
        - currentWishlistSize = random.randint(1, 50) for adds
        - WishlistActionEvent auto-generates timestamp

        Returns:
            WishlistActionEvent: A validated wishlist event
        """
        games, weights = get_weighted_game_choices()
        game = random.choices(games, weights=weights)[0]
        userId = f"user_{random.randint(1000, 9999)}"
        action = random.choices(["added", "removed"], weights=[0.8, 0.2])[0]
        currentWishlistSize = random.randint(1, 50) if action == "added" else random.randint(0, 49)
        return WishlistActionEvent(
            userId=userId, 
            gameId=game["gameId"], 
            action=action, 
            currentWishlistSize=currentWishlistSize
        )

    def generate_cart_action_event(self) -> CartActionEvent:
        """
        Generate a cart action event (add or remove).

        TODO(human): Implement this function.

        Requirements:
        - Generate random userId
        - Select random game from catalog
        - 85% "added", 15% "removed" (cart adds more common than removes)
        - Calculate realistic currentCartValue (sum of items in cart)
          - If added: increase by game price (range: $0-$300)
          - If removed: decrease (range: $0-$200)
        - Calculate itemsInCart (1-10 items typically)

        Hints:
        - For added: value could be game.price * random.randint(1, 5)
        - For removed: value could be game.price * random.randint(0, 3)
        - itemsInCart should match action (add = 1-10, remove = 0-9)
        - CartActionEvent requires: userId, gameId, action, currentCartValue, itemsInCart

        Returns:
            CartActionEvent: A validated cart event
        """
        games, weights = get_weighted_game_choices()
        game = random.choices(games, weights=weights)[0]
        userId = f"user_{random.randint(1000, 9999)}"
        action = random.choices(["added", "removed"], weights=[0.85, 0.15])[0]
        currentCartValue = game["price"] * random.randint(1, 5) if action == "added" else game["price"] * random.randint(0, 3)
        itemsInCart = random.randint(1, 10) if action == "added" else random.randint(0, 9)
        return CartActionEvent(
            userId=userId, 
            gameId=game["gameId"], 
            action=action, 
            currentCartValue=currentCartValue, 
            itemsInCart=itemsInCart
        )

    def generate_purchase_event(self) -> PurchaseEvent:
        """
        Generate a purchase event (completed checkout).

        TODO(human): Implement this function.

        Requirements:
        - Generate random userId
        - Generate unique orderId (format: "order_<random_alphanumeric>")
        - Select 1-3 games for purchase (most orders are 1-2 items)
        - Create list of PurchaseItem objects: [PurchaseItem(gameId=..., price=...)]
        - Calculate totalAmount (sum of all game prices)
        - Select payment method (credit_card=50%, paypal=25%, steam_wallet=20%, crypto=5%)
        - Select region (US=40%, UK=15%, JP=10%, DE=8%, others=27%)

        Hints:
        - orderId: f"order_{random.randint(100000, 999999)}"
        - Weighted games: num_games = random.choices([1,2,3], weights=[60,30,10])[0]
        - Payment: random.choices(methods, weights=[50,25,20,5])[0]
        - Regions: random.choices(["US","UK","JP","DE","FR"], weights=[40,15,10,8,27])
        - PurchaseEvent requires: userId, orderId, games, totalAmount, paymentMethod, region

        Returns:
            PurchaseEvent: A validated purchase event
        """
        games, weights = get_weighted_game_choices()
        games = random.choices(games, weights=weights, k=random.randint(1, 3))
        userId = f"user_{random.randint(1000, 9999)}"
        orderId = f"order_{random.randint(100000, 999999)}"
        totalAmount = sum(game["price"] for game in games)
        paymentMethod = random.choices(["credit_card", "paypal", "steam_wallet", "cryptocurrency"], weights=[0.5, 0.25, 0.2, 0.05])[0]
        region = random.choices(["US", "UK", "JP", "DE", "FR"], weights=[0.4, 0.15, 0.1, 0.08, 0.27])[0]
        games = [PurchaseItem(gameId=game["gameId"], price=game["price"]) for game in games]
        return PurchaseEvent(
            userId=userId, 
            orderId=orderId, 
            games=games, 
            totalAmount=totalAmount, 
            paymentMethod=paymentMethod, 
            region=region
        )

    def generate_search_event(self) -> SearchPerformedEvent:
        """
        Generate a search performed event.

        TODO(human): Implement this function.

        Requirements:
        - Generate random userId
        - Select searchQuery from common search terms (use SEARCH_QUERIES from game_catalog)
        - Or generate realistic query: category name, tag, or game type
        - Calculate resultsCount (realistic range: 0-100)
          - Popular queries: 20-80 results
          - Obscure queries: 0-10 results
        - Select 0-3 filterTags that user applied (e.g., ["RPG", "open-world"])

        Hints:
        - Import SEARCH_QUERIES from data.game_catalog
        - searchQuery = random.choice(SEARCH_QUERIES)[0]  # [0] gets query, not weight
        - resultsCount = random.randint(5, 80) for popular queries
        - filterTags = random.sample(all_tags, k=random.randint(0, 3))
        - SearchPerformedEvent requires: userId, searchQuery, resultsCount, filterTags

        Returns:
            SearchPerformedEvent: A validated search event
        """
        userId = f"user_{random.randint(1000, 9999)}"
        searchQuery = random.choice(SEARCH_QUERIES)[0]
        resultsCount = random.randint(5, 80)
        filterTags = random.sample(CATEGORIES, k=random.randint(0, 3))
        return SearchPerformedEvent(
            userId=userId, 
            searchQuery=searchQuery, 
            resultsCount=resultsCount, 
            filterTags=filterTags
        )

    def build_event_generators(self):
        return {
            "game_page_viewed": self.generate_game_view_event,
            "wishlist_action": self.generate_wishlist_action_event,
            "cart_action": self.generate_cart_action_event,
            "purchase": self.generate_purchase_event,
            "search_performed": self.generate_search_event,
        }

    def generate_random_event(self) -> tuple[BaseModel, str, str]:
        """
        Generate a random event based on weighted probabilities.
        Returns tuple of (event_model, topic_name, event_type).
        """
        # Select event type based on weights
        event_types = list(self.EVENT_WEIGHTS.keys())
        weights = list(self.EVENT_WEIGHTS.values())
        event_type = random.choices(event_types, weights=weights)[0]
        event_generator = self.build_event_generators()[event_type]
        event = event_generator()
        topic = self.EVENT_TYPE_TO_TOPIC[event_type]
        self.event_counts[event_type] += 1
        return event, topic, event_type

    def run(self, events_per_second: int = 25, duration_seconds: int = 60):
        """
        Run the multi-event generator.

        Args:
            events_per_second: Rate of total event generation (all types combined)
            duration_seconds: How long to run (None = run forever)
        """
        print("🚀 Starting multi-event producer...")
        print(f"📊 Rate: {events_per_second} events/second (all types)")
        print(f"⏱️  Duration: {duration_seconds}s" if duration_seconds else "⏱️  Duration: Forever")
        print(f"🎯 Topics: {len(self.EVENT_TYPE_TO_TOPIC)} topics\n")

        start_time = time.time()
        sleep_interval = 1.0 / events_per_second

        try:
            while True:
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                # Generate random event
                event, topic, event_type = self.generate_random_event()

                if event:
                    event_dict = event.model_dump()
                    self.send_event(
                        topic=topic,
                        event=event_dict,
                        key=event.userId,
                    )

                time.sleep(sleep_interval)

        except KeyboardInterrupt:
            print("\n⏸️  Stopping producer (Ctrl+C pressed)...")

        finally:
            print("\n🔄 Flushing remaining messages...")
            self.producer.flush(timeout=10)

            elapsed = time.time() - start_time
            print("\n📈 Final Stats:")
            print(f"   • Total events sent: {self.events_sent}")
            print(f"   • Errors: {self.errors}")
            print(f"   • Duration: {elapsed:.1f}s")
            print(f"   • Rate: {self.events_sent / elapsed:.1f} events/sec")
            print("\n📊 Event Breakdown:")
            for event_type, count in self.event_counts.items():
                pct = (count / self.events_sent * 100) if self.events_sent > 0 else 0
                print(f"   • {event_type}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    producer = MultiEventProducer()

    # Run for 60 seconds at 25 events/second (1500 total events)
    # This simulates realistic store traffic with all event types
    producer.run(events_per_second=25, duration_seconds=60)
