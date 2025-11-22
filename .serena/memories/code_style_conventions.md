# Code Style & Conventions

## Python Style
- **Formatter**: Black (default settings)
- **Linter**: Ruff
- **Type Checker**: Mypy
- **Naming Convention**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Module-level docstrings present, function docstrings for public methods

## Code Organization Patterns

### Configuration
- Centralized in `config/kafka_config.py`
- Constants in UPPER_SNAKE_CASE
- Typed dictionaries for configs using `Dict[str, Any]`

### Event Schemas
- Pydantic models for event validation (`event_schemas.py`)
- Dataclasses with type hints
- Event naming: `{Action}{Entity}Event` (e.g., `GamePageViewedEvent`)

### Kafka Configuration Patterns
```python
PRODUCER_CONFIG = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "acks": "all",
    "retries": 3,
    "compression.type": "snappy",
}
```

### Topic Naming
- Pattern: `{domain}.{entity}` (e.g., `store.game-views`, `analytics.metrics`)
- Store events: `store.*`
- Analytics output: `analytics.*`

## Project Structure Conventions
- `config/`: Configuration and settings
- `producers/`: Event generation and Kafka producers
- `consumers/`: Stream processors and consumers
- `dashboard/`: Web UI and API
- `data/`: Static data files (game catalog)
- `scripts/`: Utility scripts for setup/admin tasks

## Type Hints
- Type hints used extensively
- Import from `typing` module: `Dict`, `Any`, `List`
- Pydantic models for data validation
