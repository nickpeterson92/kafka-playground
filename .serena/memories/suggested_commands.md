# Suggested Commands

## Kafka Cluster Management

### Start Kafka (Required First Step)
```bash
docker-compose up -d
```
Starts Kafka, Zookeeper, and Kafka UI in detached mode.

### Check Kafka Status
```bash
docker-compose ps
```
All three services (kafka, zookeeper, kafka-ui) should show "Up".

### Stop Kafka
```bash
docker-compose down
```

### Stop Kafka + Remove Data (Fresh Start)
```bash
docker-compose down -v
```
Removes volumes to start with clean state.

### View Kafka Logs
```bash
docker-compose logs -f kafka
docker-compose logs -f zookeeper
```

## Topic Management

### Create Kafka Topics
```bash
python scripts/setup_topics.py
```
Creates all required topics (store.*, analytics.*). Run after starting Kafka.

### View Topics in Browser
Open http://localhost:8080 (Kafka UI)

## Running Components

### Run Event Producer
```bash
python producers/event_generator.py
```
Generates simulated store events (views, wishlist, cart, purchases, searches).

### Run Analytics Consumer
```bash
python consumers/basic_consumer.py
```
Processes events and generates metrics.

### Run Dashboard (Not Yet Implemented)
```bash
python dashboard/app.py
```
Start FastAPI dashboard server on http://localhost:8000.

## Code Quality

### Format Code
```bash
black .
```

### Lint Code
```bash
ruff check .
```

### Type Check
```bash
mypy .
```

### Run Tests
```bash
pytest
```

## Darwin System Utilities
Standard Unix commands available on macOS:
- `ls`, `cd`, `pwd`: File navigation
- `grep`, `find`: Search utilities  
- `git`: Version control
- `cat`, `less`, `tail -f`: File viewing
