"""
Sample game catalog for event generation.
Based on real Steam games for realistic simulation.
"""

from typing import List, Dict, Any
import random


GAME_CATALOG: List[Dict[str, Any]] = [
    {
        "gameId": "game_001",
        "name": "Cyberpunk 2077",
        "category": "RPG",
        "price": 59.99,
        "tags": ["open-world", "story-rich", "cyberpunk"],
        "popularity": 85,  # Used for weighted sampling (higher = more views)
    },
    {
        "gameId": "game_002",
        "name": "Elden Ring",
        "category": "Action",
        "price": 59.99,
        "tags": ["souls-like", "open-world", "fantasy"],
        "popularity": 90,
    },
    {
        "gameId": "game_003",
        "name": "Stardew Valley",
        "category": "Simulation",
        "price": 14.99,
        "tags": ["farming", "relaxing", "pixel-art"],
        "popularity": 70,
    },
    {
        "gameId": "game_004",
        "name": "Counter-Strike 2",
        "category": "FPS",
        "price": 0.00,
        "tags": ["competitive", "multiplayer", "tactical"],
        "popularity": 95,  # F2P games get high traffic
    },
    {
        "gameId": "game_005",
        "name": "Baldur's Gate 3",
        "category": "RPG",
        "price": 59.99,
        "tags": ["story-rich", "party-based", "fantasy"],
        "popularity": 88,
    },
    {
        "gameId": "game_006",
        "name": "Hades",
        "category": "Roguelike",
        "price": 24.99,
        "tags": ["action", "roguelike", "mythology"],
        "popularity": 75,
    },
    {
        "gameId": "game_007",
        "name": "The Witcher 3",
        "category": "RPG",
        "price": 39.99,
        "tags": ["open-world", "story-rich", "fantasy"],
        "popularity": 82,
    },
    {
        "gameId": "game_008",
        "name": "Factorio",
        "category": "Strategy",
        "price": 30.00,
        "tags": ["automation", "building", "management"],
        "popularity": 65,
    },
    {
        "gameId": "game_009",
        "name": "Terraria",
        "category": "Sandbox",
        "price": 9.99,
        "tags": ["2D", "crafting", "adventure"],
        "popularity": 72,
    },
    {
        "gameId": "game_010",
        "name": "Portal 2",
        "category": "Puzzle",
        "price": 19.99,
        "tags": ["puzzle", "co-op", "comedy"],
        "popularity": 68,
    },
    {
        "gameId": "game_011",
        "name": "Red Dead Redemption 2",
        "category": "Action",
        "price": 59.99,
        "tags": ["open-world", "western", "story-rich"],
        "popularity": 86,
    },
    {
        "gameId": "game_012",
        "name": "Hollow Knight",
        "category": "Metroidvania",
        "price": 14.99,
        "tags": ["platformer", "challenging", "atmospheric"],
        "popularity": 73,
    },
    {
        "gameId": "game_013",
        "name": "Among Us",
        "category": "Party",
        "price": 4.99,
        "tags": ["multiplayer", "social-deduction", "casual"],
        "popularity": 62,
    },
    {
        "gameId": "game_014",
        "name": "Valheim",
        "category": "Survival",
        "price": 19.99,
        "tags": ["co-op", "crafting", "exploration"],
        "popularity": 78,
    },
    {
        "gameId": "game_015",
        "name": "Doom Eternal",
        "category": "FPS",
        "price": 39.99,
        "tags": ["fast-paced", "shooter", "demon-slaying"],
        "popularity": 80,
    },
]

# Categories for search/browse simulation
CATEGORIES = ["RPG", "Action", "Simulation", "FPS", "Roguelike", "Strategy", "Sandbox", "Puzzle", "Metroidvania", "Party", "Survival"]

# Common search queries (weighted by frequency)
SEARCH_QUERIES = [
    ("open world rpg", 15),
    ("multiplayer fps", 12),
    ("indie games", 10),
    ("story rich", 8),
    ("roguelike", 7),
    ("co-op", 9),
    ("puzzle games", 6),
    ("simulation", 5),
    ("survival", 7),
    ("strategy", 6),
]

# Purchase sources
PURCHASE_SOURCES = ["featured_carousel", "search", "recommendation", "direct", "wishlist", "category_browse"]

# Purchase sources probabilities
PURCHASE_SOURCES_WEIGHTS = [0.4, 0.25, 0.2, 0.05, 0.1, 0.05]

def get_purchase_source() -> PURCHASE_SOURCES:
    """Get a random purchase source."""
    return random.choices(PURCHASE_SOURCES, weights=PURCHASE_SOURCES_WEIGHTS)[0]

def get_game_by_id(game_id: str) -> Dict[str, Any] | None:
    """Get game details by ID."""
    return next((game for game in GAME_CATALOG if game["gameId"] == game_id), None)


def get_games_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all games in a category."""
    return [game for game in GAME_CATALOG if game["category"] == category]


def get_weighted_game_choices() -> tuple[List[Dict[str, Any]], List[int]]:
    """Return games and their popularity weights for weighted random selection."""
    return GAME_CATALOG, [game["popularity"] for game in GAME_CATALOG]
