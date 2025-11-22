# Tech Stack

## Core Technologies
- **Python 3.x**: Primary language
- **Apache Kafka**: Stream processing platform (via Confluent Docker images)
- **Docker Compose**: Kafka cluster orchestration

## Python Dependencies

### Kafka
- `confluent-kafka[avro,json,protobuf]`: Kafka client with serialization support

### Web Framework
- `fastapi`: API server for dashboard
- `uvicorn[standard]`: ASGI server
- `sse-starlette`: Server-Sent Events for real-time updates

### Data Processing
- `pandas`: Data manipulation and analytics
- `pydantic`: Data validation and settings
- `pydantic-settings`: Environment configuration

### Development Tools
- `black`: Code formatting
- `ruff`: Linting
- `mypy`: Type checking
- `pytest`: Testing framework
- `python-dotenv`: Environment variables

## Infrastructure
- **Kafka**: localhost:9092
- **Zookeeper**: localhost:2181
- **Kafka UI**: http://localhost:8080 (provectuslabs/kafka-ui)
- **Dashboard**: http://localhost:8000 (when running)

## Docker Images
- `confluentinc/cp-zookeeper:7.6.0`
- `confluentinc/cp-kafka:7.6.0`
- `provectuslabs/kafka-ui:latest`
