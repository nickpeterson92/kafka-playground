"""
Real-time analytics stream processor for store events.
Calculates metrics and publishes aggregated data to analytics topic.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable
from collections import defaultdict
from confluent_kafka import Consumer, Producer, KafkaError
from config.kafka_config import CONSUMER_CONFIG, PRODUCER_CONFIG, TOPICS
from producers.event_schemas import (
    GamePageViewedEvent,
    WishlistActionEvent,
    CartActionEvent,
    PurchaseEvent,
    SearchPerformedEvent,
)
from pydantic import ValidationError
class AnalyticsProcessor:
    """Stream processor that calculates real-time metrics from store events."""

    def __init__(self):
        """Initialize the analytics processor with consumer, producer, and metric storage."""
        # Kafka consumer (reads from store topics)
        consumer_config = CONSUMER_CONFIG.copy()
        consumer_config["group.id"] = "analytics-processor"
        self.consumer = Consumer(consumer_config)
        
        # Kafka producer (writes to analytics topic)
        self.producer = Producer(PRODUCER_CONFIG)
        
        # Subscribe to all store event topics
        self.consumer.subscribe([
            TOPICS["game_views"],
            TOPICS["wishlist_events"],
            TOPICS["cart_events"],
            TOPICS["purchases"],
            TOPICS["searches"],
        ])
        
        # Metric storage - track events and calculations
        self.reset_metrics()
        
        # Timing control for 10-second output intervals
        self.last_publish_time = time.time()
        self.publish_interval = 10  # seconds
        
        print("Analytics Processor initialized")
        print(f"Publishing metrics every {self.publish_interval} seconds\n")

    def reset_metrics(self):
        """Reset all metric counters (called after publishing)."""
        # Event counters by type
        self.event_counts = defaultdict(int)
        
        # Revenue tracking
        self.total_revenue = 0.0
        self.purchase_count = 0
        
        # Game tracking for trending analysis
        self.game_views = defaultdict(int)  # gameId -> view count
        self.game_purchases = defaultdict(int)  # gameId -> purchase count
        
        # Conversion funnel counters
        self.funnel_views = 0
        self.funnel_wishlist_adds = 0
        self.funnel_cart_adds = 0
        self.funnel_purchases = 0
        
        # Window start time (for calculating rates)
        self.window_start_time = time.time()

    def handle_game_page_viewed_event(self, event_data: GamePageViewedEvent) -> None:
        self.funnel_views += 1
        self.game_views[event_data.gameId] += 1

    def handle_wishlist_action_event(self, event_data: WishlistActionEvent) -> None:
        if event_data.action == "added":
            self.funnel_wishlist_adds += 1

    def handle_cart_action_event(self, event_data: CartActionEvent) -> None:
        if event_data.action == "added":
            self.funnel_cart_adds += 1

    def handle_purchase_event(self, event_data: PurchaseEvent) -> None:
        self.funnel_purchases += 1
        self.total_revenue += event_data.totalAmount
        self.purchase_count += 1
        for game in event_data.games:
            self.game_purchases[game.gameId] += 1

    def handle_search_performed_event(self, event_data: SearchPerformedEvent) -> None:
        pass

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
        Process a single event and update metrics.
        
        Args:
            event_data: Dictionary containing the event fields
        """
        
        # TODO(human): Process different event types and update metrics
        # 
        # Implement the metric updates for each event type:
        # 
        # 1. game_page_viewed:
        #    - Increment funnel_views
        #    - Track game_views[gameId]
        # 
        # 2. wishlist_action (only for "added" actions):
        #    - Increment funnel_wishlist_adds
        # 
        # 3. cart_action (only for "added" actions):
        #    - Increment funnel_cart_adds
        # 
        # 4. purchase:
        #    - Increment funnel_purchases
        #    - Add to total_revenue (use event_data["totalAmount"])
        #    - Increment purchase_count
        #    - Track game_purchases for each game in the purchase
        #      (Hint: event_data["games"] is a list of dicts with "gameId")
        # 
        # 5. search_performed:
        #    - Already counted in event_counts, no extra tracking needed
        event_type_map = {
            "game_page_viewed": GamePageViewedEvent,
            "wishlist_action": WishlistActionEvent,
            "cart_action": CartActionEvent,
            "purchase": PurchaseEvent,
            "search_performed": SearchPerformedEvent,
        }
        event_type = event_data.get("eventType")
        event_model = event_type_map[event_type](**event_data)
        event_handlers = self.build_event_handlers()
        handler = event_handlers.get(type(event_model))
        if handler:
            handler(event_model)
        else:
            print(f"No handler for {type(event_model)}")

            
    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate aggregated metrics from collected data.
        
        Returns:
            Dictionary containing all calculated metrics
        """
        # Calculate time window duration
        window_duration_seconds = time.time() - self.window_start_time
        window_duration_minutes = window_duration_seconds / 60.0
        
        # TODO(human): Calculate metrics and return as dictionary
        # 
        # Calculate and return these metrics:
        # 
        # 1. revenue_per_minute: total_revenue / window_duration_minutes
        # 2. events_per_minute: dict with each event type's rate
        #    (event_counts[type] / window_duration_minutes for each type)
        # 3. conversion_rates: Calculate funnel percentages
        #    - view_to_wishlist: (funnel_wishlist_adds / funnel_views * 100) if funnel_views > 0
        #    - wishlist_to_cart: (funnel_cart_adds / funnel_wishlist_adds * 100) if funnel_wishlist_adds > 0
        #    - cart_to_purchase: (funnel_purchases / funnel_cart_adds * 100) if funnel_cart_adds > 0
        #    - overall_conversion: (funnel_purchases / funnel_views * 100) if funnel_views > 0
        # 4. trending_games: Top 5 most viewed games
        #    (Hint: sorted(game_views.items(), key=lambda x: x[1], reverse=True)[:5])
        # 5. top_purchases: Top 5 most purchased games (same approach as trending)
        # 6. average_order_value: total_revenue / purchase_count if purchase_count > 0
        # 
        # Return format:
        # {
        #     "timestamp": current ISO timestamp,
        #     "window_duration_seconds": window_duration_seconds,
        #     "revenue_per_minute": ...,
        #     "events_per_minute": {...},
        #     "conversion_rates": {...},
        #     "trending_games": [...],
        #     "top_purchases": [...],
        #     "average_order_value": ...
        # }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "window_duration_seconds": window_duration_seconds,
            "revenue_per_minute": self.total_revenue / window_duration_minutes,
            "events_per_minute": {event_type: self.event_counts[event_type] / window_duration_minutes for event_type in self.event_counts},
            "conversion_rates": {
                "view_to_wishlist": self.funnel_wishlist_adds / self.funnel_views * 100 if self.funnel_views > 0 else 0,
                "wishlist_to_cart": self.funnel_cart_adds / self.funnel_wishlist_adds * 100 if self.funnel_wishlist_adds > 0 else 0,
                "cart_to_purchase": self.funnel_purchases / self.funnel_cart_adds * 100 if self.funnel_cart_adds > 0 else 0,
                "overall_conversion": self.funnel_purchases / self.funnel_views * 100 if self.funnel_views > 0 else 0,
            },
            "trending_games": sorted(self.game_views.items(), key=lambda x: x[1], reverse=True)[:5],
            "top_purchases": sorted(self.game_purchases.items(), key=lambda x: x[1], reverse=True)[:5],
            "average_order_value": self.total_revenue / self.purchase_count if self.purchase_count > 0 else 0,
        }

    def publish_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Publish calculated metrics to the analytics topic.
        
        Args:
            metrics: Dictionary containing all metrics to publish
        """
        try:
            # Convert metrics to JSON
            metrics_json = json.dumps(metrics)
            
            # Produce to analytics topic
            self.producer.produce(
                TOPICS["analytics"],
                key="metrics",
                value=metrics_json,
                callback=self.delivery_callback
            )
            
            # Flush to ensure delivery
            self.producer.flush()
            
        except Exception as e:
            print(f"❌ Error publishing metrics: {e}")

    def delivery_callback(self, err, msg):
        """Callback for message delivery confirmation."""
        if err:
            print(f"❌ Delivery failed: {err}")
        else:
            print(f"✅ Metrics published to {msg.topic()}")

    def print_metrics_summary(self, metrics: Dict[str, Any]) -> None:
        """Print a formatted summary of current metrics to console."""
        print("\n" + "="*60)
        print(f"📊 ANALYTICS SUMMARY - {metrics.get('timestamp', 'N/A')}")
        print("="*60)
        
        # Revenue metrics
        print("\n💰 REVENUE:")
        print(f"   Revenue/min: ${metrics.get('revenue_per_minute', 0):.2f}")
        print(f"   Avg order value: ${metrics.get('average_order_value', 0):.2f}")
        
        # Event rates
        print("\n📈 EVENT RATES (per minute):")
        events_per_min = metrics.get('events_per_minute', {})
        for event_type, rate in events_per_min.items():
            print(f"   {event_type}: {rate:.1f}")
        
        # Conversion funnel
        print("\n🎯 CONVERSION FUNNEL:")
        conv = metrics.get('conversion_rates', {})
        print(f"   View → Wishlist: {conv.get('view_to_wishlist', 0):.2f}%")
        print(f"   Wishlist → Cart: {conv.get('wishlist_to_cart', 0):.2f}%")
        print(f"   Cart → Purchase: {conv.get('cart_to_purchase', 0):.2f}%")
        print(f"   Overall: {conv.get('overall_conversion', 0):.2f}%")
        
        # Trending games
        print("\n🔥 TRENDING GAMES (Most Viewed):")
        for game_id, count in metrics.get('trending_games', [])[:3]:
            print(f"   {game_id}: {count} views")
        
        print("="*60 + "\n")

    def run(self):
        """Main processing loop - consume events and publish metrics periodically."""
        print("Starting analytics processor...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Poll for new messages
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    # No message available
                    pass
                elif msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"❌ Consumer error: {msg.error()}")
                        continue
                else:
                    # Successfully received a message
                    try:
                        event_json = msg.value().decode("utf-8")
                        event_data = json.loads(event_json)
                        
                        # Process the event
                        self.process_event(event_data)
                        
                        # Commit offset
                        self.consumer.commit(asynchronous=False)
                        
                    except Exception as e:
                        print(f"❌ Error processing event: {e}")
                
                # Check if it's time to publish metrics (every 10 seconds)
                current_time = time.time()
                if current_time - self.last_publish_time >= self.publish_interval:
                    # Calculate metrics
                    metrics = self.calculate_metrics()
                    
                    # Print summary to console
                    self.print_metrics_summary(metrics)
                    
                    # Publish to Kafka
                    self.publish_metrics(metrics)
                    
                    # Reset for next window
                    self.reset_metrics()
                    self.last_publish_time = current_time
        
        except KeyboardInterrupt:
            print("\n\nStopping analytics processor...")
        
        finally:
            print("Closing connections...")
            self.consumer.close()
            self.producer.flush()
            print("Analytics processor stopped.")


if __name__ == "__main__":
    processor = AnalyticsProcessor()
    processor.run()
