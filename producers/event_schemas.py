"""
Event schema definitions using Pydantic for validation.
Each event type has a model that ensures data integrity.
"""

from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime


class GamePageViewedEvent(BaseModel):
    """Tracks when a user views a game's store page."""

    eventType: Literal["game_page_viewed"] = "game_page_viewed"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    userId: str
    gameId: str
    gameName: str
    price: float
    onSale: bool = False
    salePrice: float | None = None
    category: str
    tags: List[str]
    source: Literal[
        "featured_carousel", "search", "recommendation", "direct", "wishlist", "category_browse"
    ]


class WishlistActionEvent(BaseModel):
    """Tracks additions/removals from user wishlists."""

    eventType: Literal["wishlist_action"] = "wishlist_action"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    userId: str
    gameId: str
    action: Literal["added", "removed"]
    currentWishlistSize: int


class CartActionEvent(BaseModel):
    """Tracks items being added/removed from shopping cart."""

    eventType: Literal["cart_action"] = "cart_action"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    userId: str
    gameId: str
    action: Literal["added", "removed"]
    currentCartValue: float
    itemsInCart: int


class PurchaseItem(BaseModel):
    """Single item in a purchase."""

    gameId: str
    price: float


class PurchaseEvent(BaseModel):
    """Tracks completed purchases (checkout success)."""

    eventType: Literal["purchase"] = "purchase"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    userId: str
    orderId: str
    games: List[PurchaseItem]
    totalAmount: float
    paymentMethod: Literal["credit_card", "paypal", "steam_wallet", "cryptocurrency"]
    region: str  # ISO country code


class SearchPerformedEvent(BaseModel):
    """Tracks user searches in the store."""

    eventType: Literal["search_performed"] = "search_performed"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    userId: str
    searchQuery: str
    resultsCount: int
    filterTags: List[str] = Field(default_factory=list)
